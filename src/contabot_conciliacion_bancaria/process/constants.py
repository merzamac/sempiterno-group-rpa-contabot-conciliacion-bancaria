DASHED_DAY_FIRST_DATE_FORMAT = "%d-%m-%Y %H:%M:%S"

# Definimos nuestros conjuntos de filtro
MONEDAS: dict = {"USD": "US$", "PEN": "S/"}  # Dólares y Soles
BANKS: tuple = ("BCP", "IBK", "BBVA", "SBK")  # Los 4 bancos
PAYMENT_GATEWAYS_POSIBILITES: tuple = (
    "EXPRESS",
    # "OTROS",
    "AMERICAN EXPRESS",
    "MASTERCARD",
    "MASTER",
    "CARD",
    "AMERICAN",
    "EFECTIVO",
    # "OTROS INGRESOS",
    # "CITIBANK",
)
MAX_ROWS = 990  # para excel de mas de 1000 filas en los masivos ingresos

CUENTA_CONTABLE_USD = {
    "BBVA": 104142,
    "SBK": 104114,
    "IBK": 104132,
    "BCP": 104122,
}
CUENTA_CONTABLE_PEN = {
    "BBVA": 104141,
    "SBK": 104113,
    "IBK": 104131,
    "BCP": 104121,
}

# una fila del dataframe se considera vacia si hay mas de 3 campos vacios
EMPTY_ROW_IDICATOR = 3
