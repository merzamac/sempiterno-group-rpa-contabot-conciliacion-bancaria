from contabot_conciliacion_bancaria.processor.strategy import (
    ProcessProcessor,
    AppBasedProcessor,
)
from contabot_conciliacion_bancaria.path_reader.domain.models import (
    ProcessableFile,
    ProcessableDirectory,
)
from pathlib import Path
from contabot_conciliacion_bancaria.process.conciliacion.infrastructure.repositories import (
    ConciliacionContainer,
)
from contabot_conciliacion_bancaria.process.shared.domain.repositories import Container


class ConciliacionProcessor(AppBasedProcessor):
    def get_container(self, element_path: Path) -> Container:
        return ConciliacionContainer(element_path)

    def process(
        self, processable_directory: ProcessableDirectory, save_directory: Path
    ) -> None:
        container = self.get_container(processable_directory.element_path)
        container.conciliar()
        container.masivo(period_date=processable_directory.get_period_date)
        container.save(save_directory)

    def process_with_app(self): ...
