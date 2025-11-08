from typing import Optional, Protocol
from abc import ABC, abstractmethod


from contabot_conciliacion_bancaria.path_reader.domain.models import (
    ProcessableDirectory,
)
from contabot_conciliacion_bancaria.process.shared.domain.repositories import Container
from pathlib import Path


class ProcessProcessor(ABC):
    """Interface para todos los procesadores de proceso"""

    @abstractmethod
    def process(
        self, processable_directory: ProcessableDirectory, save_directory: Path
    ) -> None: ...


class AppBasedProcessor(ProcessProcessor, ABC):
    """Base para procesadores que usan SIG"""

    def process(
        self, processable_directory: ProcessableDirectory, save_directory: Path
    ) -> None:
        """Implementación base común para procesadores SIG"""
        print("logica")

    @abstractmethod
    def get_container(self, element_path: Path) -> Container:
        pass
