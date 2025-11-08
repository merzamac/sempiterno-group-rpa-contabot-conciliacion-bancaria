from dataclasses import dataclass
from datetime import datetime
from typing import cast

from contabot_conciliacion_bancaria.path_reader.domain.models import (
    ProcessableElement,
    ProcessableFile,
    ProcessableDirectory,
)


@dataclass
class GetFilesToProcessCommand:
    processable_input_files: tuple[ProcessableDirectory, ...]
    processable_output_elements: tuple[ProcessableDirectory, ...]
    current_date: datetime


class GetFilesToProcess:
    @staticmethod
    def execute(command: GetFilesToProcessCommand) -> set[ProcessableDirectory]:
        input_directory_to_process: set[ProcessableDirectory] = set(
            file
            for file in command.processable_input_files
            if file.get_period_date != command.current_date
        )
        output_elements: set[ProcessableDirectory] = set(
            command.processable_output_elements
        )

        input_files: set[ProcessableDirectory] = cast(
            set[ProcessableDirectory], input_directory_to_process - output_elements
        )
        return input_files
