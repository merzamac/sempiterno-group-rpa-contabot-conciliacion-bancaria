from abc import ABC, abstractmethod
from pathlib import Path
from datetime import date
from contabot_conciliacion_bancaria.process.shared.domain.models import Child

from contabot_conciliacion_bancaria.process.shared.types import FileType


class Container(ABC):

    children: tuple[Child, ...]
    file_type: FileType

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def save(self, save_dir: Path):
        save_dir.mkdir(parents=True, exist_ok=True)

        return tuple(
            result
            for child in self.children
            if (result := child.save(save_dir=save_dir)) is not None
        )

    @abstractmethod
    def conciliar(self) -> None: ...

    def masivo(self, period_date: date) -> None: ...
