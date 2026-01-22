from calendar import c
from enum import StrEnum


class Bank(StrEnum):
    BCP = "BCP"
    IBK = "IBK"
    BBVA = "BBVA"
    SBK = "SBK"


class PaymentGateway(StrEnum):
    EFECTIVO = "EFECTIVO"
    AMERICAN_EXPRESS = "AMEX"
    MASTERCARD = "MC"

    # OTROS = "OTROS"

    @classmethod
    def from_string(cls, moneda_str: str):
        """Convierte string a Moneda enum"""
        # Limpiar y normalizar el string
        if moneda_str is None or moneda_str == "":
            raise ValueError("Moneda no válida")
        moneda_limpia = moneda_str.upper().strip()

        # Mapear diferentes representaciones
        mapeo = {
            "EXPRESS": cls.AMERICAN_EXPRESS,
            # "OTROS": cls.OTROS,
            "AMERICAN EXPRESS": cls.AMERICAN_EXPRESS,
            "AMERICAN": cls.AMERICAN_EXPRESS,
            "AMEX": cls.AMERICAN_EXPRESS,
            "MASTERCARD": cls.MASTERCARD,
            "MASTER": cls.MASTERCARD,
            "CARD": cls.MASTERCARD,
            "EFECTIVO": cls.EFECTIVO,
            "MC": cls.MASTERCARD,
            # "OTROS INGRESOS": cls.OTROS,
        }

        return mapeo[moneda_limpia].value


class Moneda(StrEnum):
    USD = "USD"
    PEN = "PEN"

    @classmethod
    def from_string(cls, moneda_str: str):
        """Convierte string a Moneda enum"""
        # Limpiar y normalizar el string
        if moneda_str is None or moneda_str == "":
            raise ValueError("Moneda no válida")
        moneda_limpia = moneda_str.upper().strip()

        # Mapear diferentes representaciones
        mapeo = {
            "US$": cls.USD,
            "USD": cls.USD,
            "U$S": cls.USD,
            "DÓLARES": cls.USD,
            "DOLARES": cls.USD,
            "/S": cls.PEN,
            "PEN": cls.PEN,
            "SOLES": cls.PEN,
            "S/": cls.PEN,
        }

        return mapeo[moneda_limpia].value

    def type(self) -> str:
        """Devuelve 'N' para PEN y 'E' para USD"""
        return "N" if self == Moneda.PEN else "E"


class CuentaContable:
    def __init__(self):
        self._data = {
            "BBVA": {Moneda.USD.value: 104142, Moneda.PEN.value: 104141},
            "SBK": {Moneda.USD.value: 104114, Moneda.PEN.value: 104113},
            "IBK": {Moneda.USD.value: 104132, Moneda.PEN.value: 104131},
            "BCP": {Moneda.USD.value: 104122, Moneda.PEN.value: 104121},
        }

    def cuenta(self, banco: str, moneda: Moneda) -> int:
        """Retorna la cuenta contable de un banco y una moneda"""
        return self._data.get(banco, {}).get(moneda)

    # MÉTODOS PARA MONEDAS
    def monedas(self) -> tuple:
        """Retorna lista de todas las monedas disponibles"""
        return tuple(moneda for moneda in Moneda)

    # MÉTODOS PARA BANCOS
    def bancos(self) -> tuple:
        """Retorna lista de todos los bancos disponibles"""
        return tuple(self._data.keys())
