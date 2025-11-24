from pathlib import Path
from dataclasses import dataclass
from shutil import move
from datetime import date

from contabot_conciliacion_bancaria.utils import report


@dataclass
class ConciliacionFiles:
    movement: Path
    report: Path


@dataclass
class ToConciliar:
    glosa: str
    fecha: date


@dataclass
class ReportToConciliar:
    report: tuple
    glosas: tuple[ToConciliar, ...]
