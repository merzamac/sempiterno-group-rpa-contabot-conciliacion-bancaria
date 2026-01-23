from pathlib import Path
import fastexcel
from polars import DataFrame, read_excel
import difflib
from contabot_conciliacion_bancaria.process.commands import ReadExcelCommand
from contabot_conciliacion_bancaria.process.constants import EMPTY_ROW_IDICATOR


class ExcelDocumentReader:
    def __init__(self, file_path: Path):
        self.file_path: Path = file_path
        self.sheet_names: list[str] = fastexcel.read_excel(file_path).sheet_names

    def search_sheet_names(
        self, word: str, n: int = 4, cutoff: float = 0.6
    ) -> list[str] | str:
        """
        Search for similar sheet names in the Excel document.

        Args:
            word (str): The word to search for.
            n (int): The number of closest matches to return. Defaults to 4.
            cutoff (float): The maximum difference between the search word and the sheet name. Defaults to 0.6.

        Returns:
            list[str]: A list of sheet names that are similar to the search word.
        """
        concidences = difflib.get_close_matches(
            word, self.sheet_names, n=n, cutoff=cutoff
        )
        if n == 1:
            return str(concidences[0])

        return concidences

    def get_sheet(self, command: ReadExcelCommand) -> DataFrame:
        df = read_excel(
            self.file_path,
            sheet_name=command.sheet_name,
            infer_schema_length=0,
            read_options=command.read_options,
            drop_empty_rows=False,
            # schema_overrides=Command.schema_overrides,
        ).select(command.header_col)
        return (
            df.head(ExcelDocumentReader.rows(df))
            .cast(command.schema_overrides)
            .with_columns(command.expr)
        )

    # def get_sheets(self, Command: ReadExcelCommand) -> dict[str, DataFrame]:
    #     return {
    #         sheet_name: read_excel(
    #             self.file_path,
    #             sheet_name=sheet_name,
    #             infer_schema_length=0,
    #             read_options=Command.read_options,
    #             schema_overrides=Command.schema_overrides,
    #         )
    #         for sheet_name in self.sheet_names
    #     }
    @staticmethod
    def rows(df: DataFrame) -> int:
        consecutive_empty_rows = 0
        cut_off_index = len(df)
        for i, row in enumerate(df.iter_rows()):
            # row_empty = all(value is None or str(value).strip() == "" for value in row)
            empty_cells = sum(
                1 for value in row if value is None or str(value).strip() == ""
            )

            if empty_cells > EMPTY_ROW_IDICATOR:
                consecutive_empty_rows += 1
                if consecutive_empty_rows >= 2:
                    cut_off_index = i - 1
                    break
            else:
                consecutive_empty_rows = 0
        return cut_off_index
