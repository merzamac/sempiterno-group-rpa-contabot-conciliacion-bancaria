from contabot_conciliacion_bancaria.process.shared.domain.models import RowMasivo
from contabot_conciliacion_bancaria.types import TransactionType
from contabot_conciliacion_bancaria.process.conciliacion.app.cuenta_contable import (
    Bank,
    Moneda,
    PaymentGateway,
)
import copy
from contabot_conciliacion_bancaria.process.constants import MAX_ROWS
from .movimiento_strategy import EgresosStrategy
from .excel_builder import ReportExcelBuilder, MasivoExcelBuilder
from pathlib import Path
from dataclasses import replace
from contabot_conciliacion_bancaria.process.shared.domain.models import Child
from contabot_conciliacion_bancaria.types import SuffixTypes
from datetime import date, timedelta
from contabot_conciliacion_bancaria.process.conciliacion.types import ReportToConciliar
import calendar
from contabot_conciliacion_bancaria.utils.slice import split_operation
from contabot_conciliacion_bancaria.paths import (
    EGR_PEN_DIR,
    EGR_USD_DIR,
    MASIVOS_INGRESOS_DIR,
)


class GetReport:
    @classmethod
    def execute(
        cls,
        data_to_conciliar: ReportToConciliar,
        movements: dict,
        excel_builder: ReportExcelBuilder,
        masivo: list,
    ):
        """Método principal que orquesta todo el proceso"""
        strategy = EgresosStrategy()
        for sheet_name, movement in movements.items():
            # Procesar movimientos
            resultado = strategy.procesar(movement, data_to_conciliar)
            # Agregar sheet al Excel
            resultado["movimientos"] = movement
            masivo.extend(resultado["masivo"])
            excel_builder.make_report(sheet_name, resultado)
            # Eliminar de mayor a menor
            for i in sorted(resultado["coincidencias"], reverse=True):
                del movement[i - 2]
            masivo.extend(movement)


class MasivoByBank:
    @staticmethod
    def execute(masivo_data: dict, save_dir: Path, children: list):
        # save_dir.mkdir(parents=True, exist_ok=True)

        for sheet_name, data in masivo_data.items():
            if not data:
                continue
            masivo_excel = MasivoExcelBuilder()
            file = f"EGR {sheet_name}"
            masivo_excel.make_report(data, sheet_name)
            wb = masivo_excel.build()
            children.append(
                Child(
                    name=Path(save_dir / file),
                    wb=wb,
                    suffix=SuffixTypes.XLSX,
                    to_upload=False,
                    transaction_type="35",
                    _date=date.min,
                )
            )

            # wb.save(file)


class MasivoIngresosByBank:
    @staticmethod
    def execute(masivo_data: dict, children: list, period_date: date):
        # save_dir.mkdir(parents=True, exist_ok=True)

        for type_bank in Bank:
            ingresos_data: dict = {}
            ingresos_data = {
                sheet_name: data
                for sheet_name, data in masivo_data.items()
                if type_bank in sheet_name
            }
            num_compbte = 1
            for sheet_name, data in ingresos_data.items():
                """Dividir los movimientos en grupos, grupos por bancos. hay 4"""
                if not data:
                    continue

                for i, chuck_data in enumerate(split_operation(data, MAX_ROWS), 1):
                    """de cada banco se genera un masivo, pero tiene un limites de registros y debe ser de menos de 1000"""

                    bank = Bank[sheet_name.split(" ")[1]].value
                    masivo_excel = MasivoExcelBuilder()
                    transaction_type = f"ING PEN {bank}"
                    file = f"ING {sheet_name} {i if len(data) > 990 else ''}"
                    for j, row_data in enumerate(chuck_data, 1):
                        row_data.items = str(j).zfill(3)
                        row_data.num_compbte = str(num_compbte).zfill(2)
                    total = round(sum([row.valor_mn for row in chuck_data]), 2)
                    row_copy = copy.deepcopy(chuck_data[-1])

                    row_copy.valor_mn = total
                    row_copy.items = str(int(row_copy.items) + 1)
                    row_copy.cta_contable = (
                        "1031103" if "EFECTIVO" in sheet_name else "1031102"
                    )
                    row_copy.num_dcto = sheet_name
                    row_copy.tip_mvto = "A"
                    masivo_excel.make_report(data=(chuck_data + [row_copy]))
                    wb = masivo_excel.build()
                    children.append(
                        Child(
                            name=Path(MASIVOS_INGRESOS_DIR / bank / file),
                            wb=wb,
                            suffix=SuffixTypes.XLSX,
                            to_upload=True,
                            transaction_type=TransactionType[
                                transaction_type.replace(" ", "_")
                            ].value,
                            _date=period_date,
                        )
                    )
                    num_compbte += 1


class DuplicateMasivo:
    @staticmethod
    def execute(rows: list):
        rows_copy = [
            replace(
                row,
                items="002",
                cta_contable="011",
                tip_mvto="C",
            )
            for row in rows
        ]

        return tuple(rows + rows_copy)


class MasivoByDate:
    @staticmethod
    def execute(masivo_data: dict, save_dir: Path, children: list, period_date: date):

        # save_dir.mkdir(parents=True, exist_ok=True)
        _, last_day = calendar.monthrange(period_date.year, period_date.month)

        last_date = date(period_date.year, period_date.month, last_day)
        for sheet_name, data in masivo_data.items():
            if not data:
                continue
            first_date = date(period_date.year, period_date.month, 1)
            while first_date <= last_date:
                data_by_date = [row for row in data if row.fch_dcto == first_date]
                if not data_by_date:
                    first_date += timedelta(days=1)
                    continue
                masivo_excel = MasivoExcelBuilder()
                file = f"{first_date.strftime('%d.%m')}"
                masivo_excel.make_report(
                    data=data_by_date,
                )
                wb = masivo_excel.build()
                currency = "PEN" if "SOLES" in str(save_dir) else "USD"
                transaction_type = f"EGR {currency} {sheet_name}"
                children.append(
                    Child(
                        name=Path(save_dir / sheet_name / file),
                        wb=wb,
                        suffix=SuffixTypes.XLSX,
                        to_upload=True,
                        transaction_type=TransactionType[
                            transaction_type.replace(" ", "_")
                        ].value,
                        _date=first_date,
                    )
                )
                first_date += timedelta(days=1)
