from dataclasses import dataclass
from pathlib import Path


@dataclass
class ReadExcelCommand:
    excel_element: Path
    sheet_name: str
    read_options: dict
    schema_overrides: dict
