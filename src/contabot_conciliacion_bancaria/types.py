from enum import Enum, StrEnum


class TransactionType(StrEnum):
    """
    Tipos de transacciones bancarias con códigos.
    Formato: [TIPO] [MONEDA] [BANCO]
    TIPO: ING (Ingreso), EGR (Egreso)
    MONEDA: PEN (Soles), USD (Dólares)
    BANCO: BCP, SBK, IBK, BBVA
    """

    # BCP Transacciones
    ING_PEN_BCP = "03"
    ING_USD_BCP = "04"
    EGR_PEN_BCP = "05"
    EGR_USD_BCP = "06"

    # Scotiabank (SBK) Transacciones
    ING_PEN_SBK = "28"
    ING_USD_SBK = "29"
    EGR_PEN_SBK = "31"
    EGR_USD_SBK = "32"

    # Interbank (IBK) Transacciones
    EGR_PEN_IBK = "41"
    EGR_USD_IBK = "42"
    ING_PEN_IBK = "43"
    ING_USD_IBK = "44"

    # BBVA Transacciones
    EGR_PEN_BBVA = "51"
    EGR_USD_BBVA = "52"
    ING_PEN_BBVA = "53"
    ING_USD_BBVA = "54"


class ProcessTypes(Enum):
    CONCILIACION = "CONCILIACION"
    # VENTAS = "VENTAS"
    # COMPRAS = "COMPRAS"
    # PLANILLAS = "PLANILLAS"

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
