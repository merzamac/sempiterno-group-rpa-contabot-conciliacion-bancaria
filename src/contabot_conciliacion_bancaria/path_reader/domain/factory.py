from pathlib import Path

from contabot_conciliacion_bancaria.path_reader.domain.models import (
    ProcessableDirectory,
    ProcessableElement,
    ProcessableFile,
)
from contabot_conciliacion_bancaria.types import (
    ProcessTypes,
    SuffixTypes,
)


class ProcessableElementFactory:
    supported_process: tuple[str, ...] = ProcessTypes.values()
    supported_suffixes: tuple[str, ...] = SuffixTypes.values()

    @classmethod
    def create_element_from_path(
        cls, element_path: Path
    ) -> ProcessableDirectory | None:
        if element_path.is_dir() and cls.__has_valid_parents(element_path):
            return ProcessableDirectory(element_path)

        if element_path.is_file() and cls.__is_a_valid_processable_file(element_path):
            return ProcessableDirectory(element_path)

        return None

    @classmethod
    def create_file_from_path(cls, file_path: Path) -> ProcessableDirectory | None:
        # if not file_path.is_file():
        #    return None

        if not cls.__is_a_valid_processable_file(file_path):
            return None
        return ProcessableDirectory(file_path)

    @classmethod
    def __has_valid_parents(cls, file_path: Path) -> bool:
        parents_file: tuple[str, ...] = tuple(file_path.parts[::-1])

        has_enough_parts: bool = len(parents_file) == 5

        if not has_enough_parts:
            return False

        # has_a_valid_process: bool = (
        #     parents_file[0].strip().upper() in cls.supported_process
        # )
        has_a_valid_day_dir: bool = len(parents_file[0].strip()) == 2
        has_a_valid_month_dir: bool = len(parents_file[1].strip()) >= 5
        has_a_valid_year_dir: bool = len(parents_file[2].strip()) == 4
        return (
            # has_a_valid_process
            has_a_valid_day_dir
            and has_a_valid_month_dir
            and has_a_valid_year_dir
        )

    @classmethod
    def __is_a_valid_processable_file(cls, file_path: Path) -> bool:

        # has_a_valid_suffix: bool = file_path.suffix.lower() in cls.supported_suffixes

        # return has_a_valid_suffix and cls.__has_valid_parents(file_path)
        return cls.__has_valid_parents(file_path)
