from pathlib import Path
from contabot_conciliacion_bancaria.path_reader.app.read_dir import (
    ReadDir,
)
from contabot_conciliacion_bancaria.path_reader.domain.factory import (
    ProcessableElementFactory,
)
from contabot_conciliacion_bancaria.path_reader.domain.models import (
    ProcessableElement,
    ProcessableFile,
    ProcessableDirectory,
)
from contabot_conciliacion_bancaria.types import (
    ProcessTypes,
    SuffixTypes,
)


class ReadInputDir:

    @staticmethod
    def execute(input_dir: Path) -> tuple[ProcessableDirectory, ...]:
        directories_input: tuple[Path, ...] = (
            *ReadDir.execute(
                input_dir,
                f"*/{ProcessTypes.CONCILIACION.value}/*{SuffixTypes.XLSX.value}",
            ),
        )

        return tuple(
            processable_directory
            for directory in tuple(directories_input)
            if (
                processable_directory := ProcessableElementFactory.create_file_from_path(
                    directory
                )
            )
        )


class ReadOutputDir:

    @staticmethod
    def execute(output_dir: Path) -> tuple[ProcessableDirectory, ...]:
        directories_output: tuple[Path, ...] = (
            *ReadDir.execute(output_dir, f"*/{ProcessTypes.CONCILIACION.value}/*"),
        )
        return tuple(
            processable_directory
            for directory in directories_output
            if (
                processable_directory := ProcessableElementFactory.create_element_from_path(
                    directory
                )
            )
        )
