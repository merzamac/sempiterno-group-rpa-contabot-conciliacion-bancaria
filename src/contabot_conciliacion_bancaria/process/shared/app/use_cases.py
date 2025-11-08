from pathlib import Path

from polars import DataFrame, Expr

from polars import DataFrame, read_excel
from contabot_conciliacion_bancaria.process.commands import ReadExcelCommand


class ReadExcel:

    @staticmethod
    def execute(Command: ReadExcelCommand) -> DataFrame:

        df = read_excel(
            Command.excel_element,
            sheet_name=Command.sheet_name,
            infer_schema_length=0,
            read_options=Command.read_options,
            # schema_overrides=Command.schema_overrides,
            drop_empty_rows=False,
        )

        return df.head(ReadExcel.rows(df)).cast(Command.schema_overrides)

    @staticmethod
    def rows(df: DataFrame) -> int:
        consecutive_empty_rows = 0
        cut_off_index = len(df)
        for i, row in enumerate(df.iter_rows()):
            row_empty = all(value is None or str(value).strip() == "" for value in row)

            if row_empty:
                consecutive_empty_rows += 1
                if consecutive_empty_rows >= 2:
                    cut_off_index = i - consecutive_empty_rows + 1
                    break
            else:
                consecutive_empty_rows = 0
        return cut_off_index


class GetDataFrame:
    @staticmethod
    def execute(
        excel_path: Path,
        sheet_name: str,
        header_row: int,
        schema_overrides: dict,
        header_col: tuple,
        expr: Expr,
    ) -> DataFrame:
        """Lee una hoja específica de Excel con manejo de errores."""

        return (
            ReadExcel.execute(
                ReadExcelCommand(
                    excel_element=excel_path,
                    sheet_name=sheet_name,
                    read_options={"header_row": header_row},
                    schema_overrides=schema_overrides,
                )
            )
            .select(header_col)
            .with_columns(expr)
        )


class ExtractInsideDirectory:

    @staticmethod
    def execute(directory_path: Path, number_of_files: int) -> dict[str, Path]:
        if not directory_path.exists():
            raise ValueError(f"does not exist: {directory_path}")
        if not directory_path.is_dir():
            raise ValueError(f"it is not a directory: {directory_path}")

        # Verificar si hay archivos Excel antes de procesar

        excel_files = tuple(directory_path.glob("*.xlsx"))
        if not excel_files:
            raise ValueError(f"no Excel files found in directory: {directory_path}")

        if not (1 < len(excel_files) <= 2):
            raise ValueError(f"expected 2 Excel files, but found {len(excel_files)} ")

        # contenidos: ConciliacionResult
        # for file in excel_files:
        #     if file.stem.lower().startswith("reporte"):
        #         contenidos["reportes"] = file
        #     else:
        #         contenidos["movimientos"] = file
        contenidos: dict[str, Path] = {file.stem: file for file in excel_files}

        return contenidos
