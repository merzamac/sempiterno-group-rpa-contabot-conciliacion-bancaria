from abc import ABC
from datetime import date, datetime
from pathlib import Path

from dateparser import parse  # type: ignore


from contabot_conciliacion_bancaria.types import SuffixTypes


class ProcessableElement(ABC):
    """
    Base class for files that can be processed.
    Representa a los candidatos a ser procesado por el bot
    """

    __slots__ = (
        "element_path",
        "processed",
        "year",
        "month",
        "day",
        "process_type",
    )

    def __init__(self, element_path: Path) -> None:
        parents_file: tuple[str, ...] = tuple(element_path.parts[::-1])
        process_type, day, month, year = parents_file[:4]

        self.element_path: Path = element_path
        self.year: str = year
        self.month: str = month
        self.day: str = day
        self.process_type: str = process_type

    @property
    def get_period_date(self) -> date:
        """Returns the date of the period."""
        parse_date: datetime | None = parse(
            f"{self.day}/{self.month}/{self.year}", languages=["es"]
        )
        if parse_date is None:
            raise ValueError(
                f"Could not parse date from {self.day}/{self.month}/{self.year}"
            )

        return parse_date.date()

    def __hash__(self) -> int:
        return hash(
            f"{self.year}_{self.month}_{self.day}_{self.process_type}_{self.element_path.stem}"
        )

    def __eq__(self, other: object) -> bool:

        return (
            isinstance(other, ProcessableElement)
            and self.element_path.stem == other.element_path.stem
            and self.year == other.year
            and self.month == other.month
            and self.day == other.day
            and self.process_type == other.process_type
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(element_path={self.element_path}, "
            f"year={self.year}, month={self.month}, day={self.day}, "
            f"payment_gateway={self.process_type})"
        )


class ProcessableFile(ProcessableElement):
    """
    Represents a file that can be processed.
    This is used to represent the input files.
    """

    def __init__(self, element_path: Path) -> None:
        super().__init__(element_path)
        self.suffix: SuffixTypes = SuffixTypes(element_path.suffix.lower())
        self.relative_save_dir: Path = Path(
            f"{self.year}/{self.month}/{self.day}/{self.process_type}"
        )


class ProcessableDirectory(ProcessableElement):
    """
    Represents a directory that can be processed.
    This is used to represent the output directories.
    """
