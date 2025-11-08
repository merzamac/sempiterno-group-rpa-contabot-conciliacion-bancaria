from enum import Enum


class ProcessTypes(Enum):
    CONCILIACION = "CONCILIACION"
    VENTAS = "VENTAS"
    COMPRAS = "COMPRAS"
    PLANILLAS = "PLANILLAS"

    @classmethod
    def values(cls) -> tuple[str, ...]:
        return tuple(member.value for member in cls.__members__.values())


class SuffixTypes(Enum):
    XLSX = ".xlsx"
    ZIP = ".zip"
    CSV = ".csv"
    XLS = ".xls"

    @classmethod
    def values(cls) -> tuple[str, ...]:
        return tuple(member.value for member in cls.__members__.values())


class FileType(Enum):
    XLSX = ".xlsx"
    CSV = ".csv"
