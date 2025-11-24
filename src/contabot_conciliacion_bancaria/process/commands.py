from dataclasses import dataclass
from pathlib import Path

from polars import Expr


@dataclass
class ReadExcelCommand:
    sheet_name: str
    read_options: dict
    schema_overrides: dict
    header_col: tuple
    expr: Expr
