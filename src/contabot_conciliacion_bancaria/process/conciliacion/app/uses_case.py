from pathlib import Path
from contabot_conciliacion_bancaria.utils.safe_date_col import safe_date_col
from contabot_conciliacion_bancaria.process.conciliacion.app.factory import (
    get_header_model,
    get_schema,
)
from polars import DataFrame, col, Expr
from contabot_conciliacion_bancaria.process.shared.app.use_cases import (
    GetDataFrame,
    ReadExcel,
)
from datetime import date, datetime
from contabot_conciliacion_bancaria.process.conciliacion.types import (
    ConciliacionFiles,
)
from contabot_conciliacion_bancaria.process.commands import ReadExcelCommand
from contabot_conciliacion_bancaria.process.conciliacion.app.schema_overides import (
    SCHEMA_REPORTS,
    SCHEMA_MOVEMENT_BCP,
    SCHEMA_MOVEMENT_SBK,
)
from contabot_conciliacion_bancaria.process.shared.domain.models import (
    RowMovement,
    RowReport,
)
from contabot_conciliacion_bancaria.process.conciliacion.app.header import HeaderReport
from contabot_conciliacion_bancaria.process.constants import (
    DASHED_DAY_FIRST_DATE_FORMAT,
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


class GetFormatedMovements:
    @classmethod
    def execute(cls, excel_path: Path) -> tuple:
        movimientos_soles: dict = {}
        for sheet_name, header_row in SHEET_SOLES.items():
            bank = sheet_name.split(" ")[1]
            schema = get_schema(bank)
            header = get_header_model(bank)
            movimientos_soles_by_bank: DataFrame = GetDataFrame.execute(
                excel_path=excel_path,
                sheet_name=sheet_name,
                header_row=header_row,
                schema_overrides=schema,
                header_col=tuple(schema),
                expr=safe_date_col([header.FECHA]),
            )
            rows_movements = tuple(movimientos_soles_by_bank.to_dicts())
            rows_by_bank = []
            for row_movement in rows_movements:
                row = cls._parse_movement_transaction(row_movement, "S/", bank, header)
                rows_by_bank.append(row)

            movimientos_soles[sheet_name] = tuple(rows_by_bank)

        movimientos_dolares: dict = {}
        for sheet_name, header_row in SHEET_DOLARES.items():
            bank = sheet_name.split(" ")[1]
            schema = get_schema(bank)
            header = get_header_model(bank)
            movimientos_dolares_by_bank: DataFrame = GetDataFrame.execute(
                excel_path=excel_path,
                sheet_name=sheet_name,
                header_row=header_row,
                schema_overrides=schema,
                header_col=tuple(schema),
                expr=safe_date_col([header.FECHA]),
            )
            rows_movements = tuple(movimientos_dolares_by_bank.to_dicts())
            rows_by_bank = []
            for row_movement in rows_movements:
                row = cls._parse_movement_transaction(row_movement, "US$", bank, header)
                rows_by_bank.append(row)
            # movimientos_dolares[sheet_name] = (
            #     cls._parse_movement_transaction(row_movement, "US$", bank, header)
            #     for row_movement in rows_movements
            # )
            movimientos_dolares[sheet_name] = tuple(rows_by_bank)
        return movimientos_soles, movimientos_dolares

    @classmethod
    def _parse_movement_transaction(
        cls, row: dict, moneda: str, bank: str, header
    ) -> RowMovement:
        emision = row.get(header.FECHA)
        return RowMovement(
            fecha_emision=emision.date() if emision else date.min,
            referencia=str(row.get(header.REFERENCIA, "")).strip(),
            descripcion=str(row.get(header.DESCRIPCION, "")).strip(),
            # movimiento=str(row.get(header.MOVIMIENTO, "")),
            monto=float(row.get(header.MONTO, 0.0)),
            estado=str(row.get(header.ESTADO, "")).strip(),
            tipo_moneda=str(moneda.upper()).strip(),
            glosa=str(row.get(header.GLOSA, "")).strip(),
            banco=str(bank.strip().upper()).strip(),
        )


class GetFormatedReports:

    @classmethod
    def execute(cls, excel_path: Path) -> tuple[RowReport, ...]:
        # Leer ambas hojas
        reportes_soles = GetDataFrame.execute(
            excel_path=excel_path,
            sheet_name="SOLES",
            header_row=1,
            schema_overrides=SCHEMA_REPORTS,
            header_col=tuple(HEADER_REPORTS),
            expr=safe_date_col([HeaderReport.FECHA_EMISION, HeaderReport.FECHA_PAGO]),
        )
        reportes_dolares = GetDataFrame.execute(
            excel_path=excel_path,
            sheet_name="DÓLARES",
            header_row=4,
            schema_overrides=SCHEMA_REPORTS,
            header_col=tuple(HEADER_REPORTS),
            expr=safe_date_col([HeaderReport.FECHA_EMISION, HeaderReport.FECHA_PAGO]),
        )
        rows_reports = tuple(reportes_soles.to_dicts() + reportes_dolares.to_dicts())
        return tuple(
            cls._parse_report_transaction(row_report) for row_report in rows_reports
        )

    @classmethod
    def _parse_report_transaction(cls, row: dict) -> RowReport:
        emision = row.get(HeaderReport.FECHA_EMISION)
        fecha_pago = row.get(HeaderReport.FECHA_PAGO)
        return RowReport(  # datetime.strptime(date_value, "%Y-%m-%d").date()
            fecha_emision=emision.date() if emision else date.min,
            concatenar=str(row.get(HeaderReport.CONCATENAR, "")).strip(),
            tipo=str(row.get(HeaderReport.TIPO, "")).strip(),
            ser_doc=str(row.get(HeaderReport.SER_DOC, "")).strip(),
            numero_doc=str(row.get(HeaderReport.NUM_DOC, 0)),
            ruc=str(row.get(HeaderReport.RUC, "")),
            razon_social=str(row.get(HeaderReport.NOMBRE_RAZON_SOCIAL, "")).strip(),
            tipo_moneda=str(row.get(HeaderReport.MONEDA, "")).strip(),
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
