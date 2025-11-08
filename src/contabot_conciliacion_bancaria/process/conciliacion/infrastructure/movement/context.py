from multiprocessing.reduction import duplicate
from .movimiento_strategy import EgresosStrategy
from .excel_builder import ReportExcelBuilder, MasivoExcelBuilder
from pathlib import Path
from dataclasses import replace
from contabot_conciliacion_bancaria.process.shared.domain.models import Child
from contabot_conciliacion_bancaria.types import SuffixTypes
from datetime import date, timedelta

import calendar


class GetReport:
    @classmethod
    def execute(
        cls,
        reports: tuple,
        movements: dict,
        excel_builder: ReportExcelBuilder,
        masivo: list,
    ):
        """Método principal que orquesta todo el proceso"""
        strategy = EgresosStrategy()
        for sheet_name, movement in movements.items():
            # Procesar movimientos
            resultado = strategy.procesar(movement, reportes=reports)
            # Agregar sheet al Excel
            resultado["movimientos"] = movement
            masivo.extend(resultado["masivo"])
            excel_builder.make_report(sheet_name, resultado)


class MasivoByBank:
    @staticmethod
    def execute(masivo_data: dict, save_dir: Path, children: list):
        save_dir.mkdir(parents=True, exist_ok=True)

        for sheet_name, data in masivo_data.items():
            if not data:
                continue
            masivo_excel = MasivoExcelBuilder()
            file = f"EGR {sheet_name}"
            masivo_excel.make_report(sheet_name, data)
            wb = masivo_excel.build()
            children.append(Child(Path(save_dir / file), wb, SuffixTypes.XLSX))
            # wb.save(file)


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

        save_dir.mkdir(parents=True, exist_ok=True)
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
                masivo_excel.make_report(sheet_name, data_by_date)
                wb = masivo_excel.build()
                children.append(
                    Child(Path(save_dir / sheet_name / file), wb, SuffixTypes.XLSX)
                )
                first_date += timedelta(days=1)
