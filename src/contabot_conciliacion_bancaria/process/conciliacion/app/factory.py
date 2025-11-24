from typing import Optional
from contabot_conciliacion_bancaria.process.conciliacion.app.header import (
    Header,
    HeaderBCP,
    HeaderBBVA,
    HeaderIBK,
    HeaderSBK,
    HeaderBCPING,
    HeaderBBVAING,
    HeaderIBKING,
    HeaderSKBING,
)
from contabot_conciliacion_bancaria.process.conciliacion.app.schema_overides import (
    SCHEMA_EGRESOS_BCP,
    SCHEMA_EGRESOS_BBVA,
    SCHEMA_EGRESOS_IBK,
    SCHEMA_EGRESOS_SBK,
    SCHEMA_INGRESOS_BCP,
    SCHEMA_INGRESOS_BBVA,
    SCHEMA_INGRESOS_IBK,
    SCHEMA_INGRESOS_SKB,
)


def get_schema_egresos(type_schema: str):
    headers = {
        "BCP": SCHEMA_EGRESOS_BCP,
        "BBVA": SCHEMA_EGRESOS_BBVA,
        "IBK": SCHEMA_EGRESOS_IBK,
        "SBK": SCHEMA_EGRESOS_SBK,
    }
    column = headers.get(type_schema)
    if not column:
        raise ValueError(f"schema name no found:{type_schema}")
    return column


def get_schema_ingresos(type_schema: str):
    headers = {
        "BCP": SCHEMA_INGRESOS_BCP,
        "BBVA": SCHEMA_INGRESOS_BBVA,
        "IBK": SCHEMA_INGRESOS_IBK,
        "SBK": SCHEMA_INGRESOS_SKB,
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


def get_header_model_ingresos(type_header: str):
    headers = {
        "BCP": HeaderBCPING,
        "BBVA": HeaderBBVAING,
        "IBK": HeaderIBKING,
        "SBK": HeaderSKBING,
    }
    column = headers.get(type_header)
    if column is None:
        raise ValueError("nombre de la columna fecha del banco no encontrada...")
    return column
