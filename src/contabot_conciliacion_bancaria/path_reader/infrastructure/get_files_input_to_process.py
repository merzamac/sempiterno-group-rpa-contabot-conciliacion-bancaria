from datetime import datetime
from pathlib import Path
from typing import Generator

from contabot_conciliacion_bancaria.path_reader.app.get_files_to_process import (
    GetFilesToProcess,
    GetFilesToProcessCommand,
)
from contabot_conciliacion_bancaria.path_reader.domain.models import (
    ProcessableElement,
    ProcessableFile,
    ProcessableDirectory,
)
from contabot_conciliacion_bancaria.path_reader.infrastructure.read_dirs import (
    ReadInputDir,
    ReadOutputDir,
)


class GetInputFilesToProcess:
    @staticmethod
    def execute(
        input_dir: Path, output_dir: Path, current_date: datetime
    ) -> Generator[ProcessableDirectory, None, None]:
        processable_input_directory: tuple[ProcessableDirectory, ...] = (
            ReadInputDir.execute(input_dir=input_dir)
        )
        processable_output_directory: tuple[ProcessableDirectory, ...] = (
            ReadOutputDir.execute(output_dir=output_dir)
        )

        command: GetFilesToProcessCommand = GetFilesToProcessCommand(
            processable_input_files=processable_input_directory,
            processable_output_elements=processable_output_directory,
            current_date=current_date,
        )
        input_files_to_process: set[ProcessableDirectory] = GetFilesToProcess.execute(
            command=command
        )

        yield from tuple(
            sorted(
                input_files_to_process,
                key=lambda input_file_to_concile: input_file_to_concile.get_period_date,
                reverse=True,
            )
        )
