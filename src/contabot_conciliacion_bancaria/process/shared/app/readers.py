from abc import ABC, abstractmethod
from pathlib import Path
from io import BytesIO
from typing import Any, Dict, List
from polars import DataFrame, read_excel, col


# Patrón Command - Interfaz simple con solo execute()
class Command(ABC):
    """
    The Command interface declares a method for executing a command.
    """

    @abstractmethod
    def execute(
        self, file_path: Path, read_options: Dict, schema_overrides: Dict
    ) -> DataFrame:
        pass


# Concrete Commands
class FastExcelReadCommand(Command):
    """
    Concrete Command for reading Excel files using FastExcel.
    """

    @staticmethod
    def execute(
        file_path: Path, read_options: Dict, schema_overrides: Dict
    ) -> DataFrame:
        df = read_excel(
            file_path,
            infer_schema_length=0,
            read_options=read_options,
            schema_overrides=schema_overrides,
        ).with_columns(
            # Limpiar apóstrofe y convertir a fecha
            col("FECHA EMISIÓN")
            .str.replace("'", "")  # Eliminar el apóstrofe
            .str.to_date("%d/%m/%Y", strict=False)
        )
        return df


# class PandasExcelReadCommand(Command):
#     """
#     Concrete Command for reading Excel files using pandas.
#     """

#     def execute(
#         self, file_path: Path, read_options: Dict, schema_overrides: Dict, header: tuple
#     ) -> DataFrame:
