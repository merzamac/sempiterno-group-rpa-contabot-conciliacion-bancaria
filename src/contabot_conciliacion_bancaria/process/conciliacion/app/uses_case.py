from math import e
from pathlib import Path


from contabot_conciliacion_bancaria.utils.filter import filter_with_combinations
from contabot_conciliacion_bancaria.utils.safe_date_col import safe_date_col
from contabot_conciliacion_bancaria.process.conciliacion.app.factory import (
    get_header_model,
    get_schema_egresos,
    get_header_model_ingresos,
    get_schema_ingresos,
)
from polars import col
from datetime import date
from contabot_conciliacion_bancaria.process.conciliacion.types import (
    ConciliacionFiles,
)
from contabot_conciliacion_bancaria.process.commands import ReadExcelCommand
from contabot_conciliacion_bancaria.process.conciliacion.app.schema_overides import (
    SCHEMA_REPORTS,
)
from contabot_conciliacion_bancaria.process.shared.domain.models import (
    RowMovement,
    RowReport,
)
from contabot_conciliacion_bancaria.process.constants import (
    BANKS,
    PAYMENT_GATEWAYS_POSIBILITES,
)
from contabot_conciliacion_bancaria.process.conciliacion.types import (
    ReportToConciliar,
    ToConciliar,
)
from contabot_conciliacion_bancaria.process.conciliacion.app.header import HeaderReport
from contabot_conciliacion_bancaria.process.constants import (
    DASHED_DAY_FIRST_DATE_FORMAT,
)
from contabot_conciliacion_bancaria.excel_reader.models import ExcelDocumentReader
from contabot_conciliacion_bancaria.process.commands import ReadExcelCommand
from contabot_conciliacion_bancaria.process.conciliacion.app.cuenta_contable import (
    Bank,
    Moneda,
)
from contabot_conciliacion_bancaria.utils.filter import search
from contabot_conciliacion_bancaria.process.conciliacion.app.cuenta_contable import (
    PaymentGateway,
)

HEADER_REPORTS = tuple(SCHEMA_REPORTS)
DATE_COL = (
    col([HeaderReport.FECHA_EMISION, HeaderReport.FECHA_PAGO])
    .str.to_datetime("%Y-%m-%d %H:%M:%S", strict=False)
    .fill_null(
        col([HeaderReport.FECHA_EMISION, HeaderReport.FECHA_PAGO]).str.to_datetime(
            "%Y-%m-%d", strict=False
        )
    )
    .fill_null(
        col([HeaderReport.FECHA_EMISION, HeaderReport.FECHA_PAGO]).str.to_datetime(
            "%d/%m/%Y", strict=False
        )
    )
)
SHEET_SOLES: dict = {
    "EGR BCP SOL": 1,
    "EGR SBK SOL": 1,
    "EGR IBK SOL": 1,
    "EGR BBVA SOL": 2,
}

SHEET_DOLARES: dict = {
    "EGR BCP DOL": 1,
    "EGR SBK DOL": 1,
    "EGR IBK DOL": 1,
    "EGR BBVA DOL": 2,
}


class GetFormatedEgresosMovement:
    @classmethod
    def execute(cls, excel_path: Path) -> tuple:
        movimientos_soles: dict = {}
        excel_reader = ExcelDocumentReader(file_path=excel_path)
        sheets_egresos_soles = tuple(excel_reader.search_sheet_names("EGR     SOL"))
        sheets_egresos_dolares = tuple(excel_reader.search_sheet_names("EGR     DOL"))
        for sheet_name in sheets_egresos_soles:
            bank = Bank[sheet_name.split(" ")[1]].value
            schema = get_schema_egresos(bank)
            header = get_header_model(bank)
            movimientos_soles_by_bank = excel_reader.get_sheet(
                ReadExcelCommand(
                    sheet_name=sheet_name,
                    read_options={"header_row": 1},
                    schema_overrides=schema,
                    header_col=tuple(schema),
                    expr=safe_date_col([header.FECHA]),
                )
            )
            rows_movements = tuple(movimientos_soles_by_bank.to_dicts())
            rows_by_bank = []
            for row_movement in rows_movements:
                row = cls._parse_movement_transaction(
                    row_movement, Moneda.PEN.value, bank, header
                )
                rows_by_bank.append(row)

            movimientos_soles[sheet_name] = tuple(rows_by_bank)

        movimientos_dolares: dict = {}
        for sheet_name in sheets_egresos_dolares:
            bank = Bank[sheet_name.split(" ")[1]].value
            schema = get_schema_egresos(bank)
            header = get_header_model(bank)
            movimientos_dolares_by_bank = excel_reader.get_sheet(
                ReadExcelCommand(
                    sheet_name=sheet_name,
                    read_options={"header_row": 1},
                    schema_overrides=schema,
                    header_col=tuple(schema),
                    expr=safe_date_col([header.FECHA]),
                )
            )
            rows_movements = tuple(movimientos_dolares_by_bank.to_dicts())
            rows_by_bank = []
            for row_movement in rows_movements:
                row = cls._parse_movement_transaction(
                    row_movement, Moneda.USD.value, bank, header
                )
                rows_by_bank.append(row)

            movimientos_dolares[sheet_name] = tuple(rows_by_bank)
        return movimientos_soles, movimientos_dolares

    @classmethod
    def _parse_movement_transaction(
        cls, row: dict, moneda: str, bank: str, header
    ) -> RowMovement:
        emision = row.get(header.FECHA)
        return RowMovement(
            fecha_pagos=emision.date() if emision else date.min,
            referencia=str(row.get(header.REFERENCIA, "")).strip().replace(" ", ""),
            descripcion=str(row.get(header.DESCRIPCION, "")).strip(),
            # movimiento=str(row.get(header.MOVIMIENTO, "")),
            tipo_transaccion="",
            monto=float(row.get(header.MONTO, 0.0)),
            estado=str(row.get(header.ESTADO, "")).strip(),
            tipo_moneda=str(moneda.upper()).strip(),
            glosa=str(row.get(header.GLOSA, "")).strip(),
            banco=str(bank.strip().upper()).strip(),
            pagos=str(row.get(header.DESCRIPCION, "")).strip(),
        )


class GetFormatedIngresosMovement:
    @classmethod
    def execute(cls, excel_path: Path) -> tuple:
        movimientos_soles: dict = {}
        excel_reader = ExcelDocumentReader(file_path=excel_path)
        sheets_ingresos_soles = tuple(excel_reader.search_sheet_names("ING     SOL"))
        # sheets_egresos_dolares = tuple(excel_reader.search_sheet_names("ING     DOL"))
        # sheets_egresos_dolares: tuple = ()
        rows_ingresos_pen: list = []
        for sheet_name in sheets_ingresos_soles:
            bank = Bank[sheet_name.split(" ")[1]].value
            schema = get_schema_ingresos(bank)
            header = get_header_model_ingresos(bank)
            movimientos_soles_by_bank = excel_reader.get_sheet(
                ReadExcelCommand(
                    sheet_name=sheet_name,
                    read_options={"header_row": 1},
                    schema_overrides=schema,
                    header_col=tuple(schema),
                    expr=safe_date_col([header.FECHA]),
                )
            )
            rows_movements = tuple(movimientos_soles_by_bank.to_dicts())
            #
            for row_movement in rows_movements:
                if not row_movement.get(header.FECHA) and not row_movement.get(
                    header.REFERENCIA
                ):
                    continue
                row = cls._parse_movement_transaction(
                    row_movement, Moneda.PEN.value, bank, header
                )
                if row.fecha_pagos == date.min:
                    continue
                rows_ingresos_pen.append(row)

            # movimientos_soles[sheet_name] = tuple(rows_ingresos)
        rows_ingresos_usd: list = []
        # movimientos_dolares: dict = {}
        # los ingresos de dolares no estan considerados para los masivos, ya lo habia echo asi que los comente
        """ for sheet_name in sheets_egresos_dolares:
            bank = sheet_name.split(" ")[1]
            schema = get_schema_ingresos(bank)
            header = get_header_model_ingresos(bank)
            movimientos_dolares_by_bank = excel_reader.get_sheet(
                ReadExcelCommand(
                    sheet_name=sheet_name,
                    read_options={"header_row": 1},
                    schema_overrides=schema,
                    header_col=tuple(schema),
                    expr=safe_date_col([header.FECHA]),
                )
            )
            rows_movements = tuple(movimientos_dolares_by_bank.to_dicts())
            rows_by_bank = []
            for row_movement in rows_movements:
                row = cls._parse_movement_transaction(row_movement, Moneda.USD.value, bank, header)
                rows_by_bank.append(row)

            movimientos_dolares[sheet_name] = tuple(rows_by_bank) """
        return tuple(rows_ingresos_pen), tuple(rows_ingresos_usd)

    @classmethod
    def _parse_movement_transaction(
        cls, row: dict, moneda: str, bank: str, header
    ) -> RowMovement:

        emision = row.get(header.FECHA)

        transaccion = str(row.get(header.METODO, "")).strip()
        posibilities = (
            tuple(member.value for member in PaymentGateway.__members__.values())
            + PAYMENT_GATEWAYS_POSIBILITES
        )

        type_transaccion = search(transaccion, posibilities, cutoff=0.6)
        if type_transaccion:
            type_transaccion = PaymentGateway.from_string(type_transaccion)

        return RowMovement(
            fecha_pagos=emision.date() if emision else date.min,
            referencia=str(row.get(header.REFERENCIA, "")).strip(),
            descripcion=str(row.get(header.DESCRIPCION, "")).strip(),
            # movimiento=str(row.get(header.MOVIMIENTO, "")),
            tipo_transaccion=type_transaccion,
            monto=float(row.get(header.MONTO, 0.0)),
            estado="",
            tipo_moneda=moneda.strip(),
            glosa=f"ING TARJETA {bank} {type_transaccion} {str(emision.date().year)[-2:] if emision else ''}",
            banco=bank,
            pagos=str(row.get(header.DESCRIPCION, "")).strip(),
        )


class GetFormatedToConciliar:

    @classmethod
    def execute(cls, excel_path: Path) -> ReportToConciliar:
        excel_reader = ExcelDocumentReader(file_path=excel_path)
        # Leer ambas hojas
        sheet_reporte_soles = excel_reader.search_sheet_names("SOLES", 1)
        sheet_reporte_dolares = excel_reader.search_sheet_names("DÓLARES", 1)
        if not isinstance(sheet_reporte_soles, str) or not isinstance(
            sheet_reporte_dolares, str
        ):
            raise Exception(
                f"Solo debe haber dos hojas SOLES y Dólares en reportes: {sheet_reporte_soles}, {sheet_reporte_dolares}"
            )

        reportes_soles = excel_reader.get_sheet(
            ReadExcelCommand(
                sheet_name=sheet_reporte_soles,
                read_options={"header_row": 1},
                schema_overrides=SCHEMA_REPORTS,
                header_col=tuple(HEADER_REPORTS),
                expr=safe_date_col(
                    [HeaderReport.FECHA_EMISION, HeaderReport.FECHA_PAGO]
                ),
            )
        )
        reportes_dolares = excel_reader.get_sheet(
            ReadExcelCommand(
                sheet_name=sheet_reporte_dolares,
                read_options={"header_row": 1},
                schema_overrides=SCHEMA_REPORTS,
                header_col=tuple(HEADER_REPORTS),
                expr=safe_date_col(
                    [HeaderReport.FECHA_EMISION, HeaderReport.FECHA_PAGO]
                ),
            )
        )
        # reportes_soles = GetDataFrame.execute(
        #     excel_path=excel_path,
        #     sheet_name="SOLES",
        #     header_row=1,
        #     schema_overrides=SCHEMA_REPORTS,
        #     header_col=tuple(HEADER_REPORTS),
        #     expr=safe_date_col([HeaderReport.FECHA_EMISION, HeaderReport.FECHA_PAGO]),
        # )
        # reportes_dolares = GetDataFrame.execute(
        #     excel_path=excel_path,
        #     sheet_name="DÓLARES",
        #     header_row=4,
        #     schema_overrides=SCHEMA_REPORTS,
        #     header_col=tuple(HEADER_REPORTS),
        #     expr=safe_date_col([HeaderReport.FECHA_EMISION, HeaderReport.FECHA_PAGO]),
        # )
        # rows_reports = []

        # rows_reports.extend(reportes_soles.to_dicts())
        # rows_reports.extend(reportes_dolares.to_dicts())
        rows_reports_soles = tuple(reportes_soles.to_dicts())
        rows_reports_dolares = tuple(reportes_dolares.to_dicts())
        reports_usd = tuple(
            cls._parse_report_transaction(row_report)
            for row_report in rows_reports_dolares
        )
        reports_pen = tuple(
            cls._parse_report_transaction(row_report)
            for row_report in rows_reports_soles
        )

        resultados: list[ToConciliar] = []
        filter_with_combinations(reports_usd, resultados)
        filter_with_combinations(reports_pen, resultados)
        # for bank in BANKS:
        #     combinaciones_vistas = set()
        #     reports_by_bank = [r for r in reports_usd if r.banco == bank]
        #     for report in reports_by_bank:
        #         combinacion = (report.pagos, report.fecha_pagos)
        #         if combinacion not in combinaciones_vistas:
        #             combinaciones_vistas.add(combinacion)
        #             resultados.append(
        #                 ToConciliar(glosa=report.pagos, fecha=report.fecha_pagos)
        #             )
        # for bank in BANKS:
        #     combinaciones_vistas = set()
        #     reports_by_bank = [r for r in reports_pen if r.banco == bank]
        #     for report in reports_by_bank:
        #         combinacion = (report.pagos, report.fecha_pagos)
        #         if combinacion not in combinaciones_vistas:
        #             combinaciones_vistas.add(combinacion)
        #             resultados.append(
        #                 ToConciliar(glosa=report.pagos, fecha=report.fecha_pagos)
        #             )

        return ReportToConciliar(
            report=(reports_usd + reports_pen), glosas=tuple(resultados)
        )

    @classmethod
    def _parse_report_transaction(cls, row: dict) -> RowReport:
        emision = row.get(HeaderReport.FECHA_EMISION)
        fecha_pago = row.get(HeaderReport.FECHA_PAGO)
        moneda = Moneda.from_string(str(row.get(HeaderReport.MONEDA, "")))
        return RowReport(  # datetime.strptime(date_value, "%Y-%m-%d").date()
            fecha_emision=emision.date() if emision else date.min,
            concatenar=str(row.get(HeaderReport.CONCATENAR, "")).strip(),
            tipo=str(row.get(HeaderReport.TIPO, "")).strip(),
            ser_doc=str(row.get(HeaderReport.SER_DOC, "")).strip(),
            numero_doc=str(row.get(HeaderReport.NUM_DOC, 0)),
            ruc=str(row.get(HeaderReport.RUC, "")),
            razon_social=str(row.get(HeaderReport.NOMBRE_RAZON_SOCIAL, "")).strip(),
            tipo_moneda=moneda,
            glosa=str(row.get(HeaderReport.GLOSA, "")).strip(),
            monto=float(row.get(HeaderReport.TOTAL, 0.0)),
            banco=str(row.get(HeaderReport.BANCO, "")).strip(),
            pagos=str(row.get(HeaderReport.PAGOS, "")).strip(),
            fecha_pagos=fecha_pago.date() if fecha_pago else date.min,
        )


class ExtractConciliacionFiles:
    @staticmethod
    def execute(excel_files: dict[str, Path]) -> ConciliacionFiles:
        return {
            ExtractConciliacionFiles.get_normalized_key(name_file): file_path
            for name_file, file_path in excel_files.items()
        }  # type: ignore

    @staticmethod
    def get_normalized_key(key: str) -> str:
        if key.lower().startswith("movimientos"):
            return "movimientos"

        return "reportes"
