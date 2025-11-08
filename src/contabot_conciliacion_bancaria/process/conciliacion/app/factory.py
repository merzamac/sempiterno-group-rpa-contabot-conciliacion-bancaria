from typing import Optional
from contabot_conciliacion_bancaria.process.conciliacion.app.header import (
    Header,
    HeaderBCP,
    HeaderBBVA,
    HeaderIBK,
    HeaderSBK,
)
from contabot_conciliacion_bancaria.process.conciliacion.app.schema_overides import (
    SCHEMA_MOVEMENT_SBK,
    SCHEMA_MOVEMENT_BCP,
    SCHEMA_MOVEMENT_IBK,
    SCHEMA_MOVEMENT_BBVA,
)


def get_schema(type_schema: str):
    headers = {
        "BCP": SCHEMA_MOVEMENT_BCP,
        "BBVA": SCHEMA_MOVEMENT_BBVA,
        "IBK": SCHEMA_MOVEMENT_IBK,
        "SBK": SCHEMA_MOVEMENT_SBK,
    }
    column = headers.get(type_schema)
    if not column:
        raise ValueError(f"schema name no found:{type_schema}")
    return column


def get_header_model(type_header: str):
    headers = {
        "BCP": HeaderBCP,
        "BBVA": HeaderBBVA,
        "IBK": HeaderIBK,
        "SBK": HeaderSBK,
    }
    column = headers.get(type_header)
    if column is None:
        raise ValueError("nombre de la columna fecha del banco no encontrada...")
    return column
