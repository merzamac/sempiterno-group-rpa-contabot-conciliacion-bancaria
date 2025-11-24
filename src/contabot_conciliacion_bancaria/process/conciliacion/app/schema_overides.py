from contabot_conciliacion_bancaria.process.conciliacion.app.header import (
    HeaderReport,
    HeaderBCP,
    HeaderSBK,
    HeaderIBK,
    HeaderBBVA,
    HeaderBBVAING,
    HeaderIBKING,
    HeaderSKBING,
    HeaderBCPING,
)
from polars import Date, Utf8, Float64, Decimal, Datetime

SCHEMA_REPORTS: dict = {
    HeaderReport.FECHA_EMISION: Utf8,  # o pl.Datetime si incluye hora
    HeaderReport.TIPO: Utf8,
    HeaderReport.CONCATENAR: Utf8,
    HeaderReport.SER_DOC: Utf8,
    HeaderReport.NUM_DOC: Utf8,
    HeaderReport.RUC: Utf8,  # String para preservar ceros a la izquierda
    HeaderReport.NOMBRE_RAZON_SOCIAL: Utf8,
    HeaderReport.GLOSA: Utf8,
    HeaderReport.MONEDA: Utf8,  # Código de moneda (PEN, USD, etc.)
    HeaderReport.TOTAL: Decimal(12, 2),  # o pl.Decimal para precisión monetaria
    HeaderReport.BANCO: Utf8,
    HeaderReport.PAGOS: Utf8,  # o pl.Float64 si son montos de pagos
    HeaderReport.FECHA_PAGO: Utf8,
    HeaderReport.REGISTRO: Utf8,
    HeaderReport.COMENTARIO: Utf8,
}

SCHEMA_EGRESOS_BCP: dict = {
    HeaderBCP.REG: Utf8,
    HeaderBCP.FECHA: Utf8,  # O Date si quieres tipo fecha directamente
    HeaderBCP.REFERENCIA: Utf8,
    HeaderBCP.DESCRIPCION: Utf8,
    HeaderBCP.MONTO: Decimal(12, 2),
    HeaderBCP.ESTADO: Utf8,
    HeaderBCP.COMENTARIO: Utf8,
    HeaderBCP.GLOSA: Utf8,
}
SCHEMA_EGRESOS_SBK: dict = {
    HeaderSBK.REG: Utf8,
    HeaderSBK.FECHA: Utf8,  # O Date si quieres tipo fecha directamente
    HeaderSBK.REFERENCIA: Utf8,
    HeaderSBK.DESCRIPCION: Utf8,
    HeaderSBK.MONTO: Decimal(12, 2),
    HeaderSBK.ESTADO: Utf8,
    HeaderSBK.COMENTARIO: Utf8,
    HeaderSBK.GLOSA: Utf8,
}
SCHEMA_EGRESOS_IBK: dict = {
    HeaderIBK.REG: Utf8,
    HeaderIBK.FECHA: Utf8,  # O Date si quieres tipo fecha directamente
    HeaderIBK.REFERENCIA: Utf8,
    HeaderIBK.DESCRIPCION: Utf8,
    HeaderIBK.MONTO: Decimal(12, 2),
    HeaderIBK.ESTADO: Utf8,
    HeaderIBK.COMENTARIO: Utf8,
    HeaderIBK.GLOSA: Utf8,
}

SCHEMA_EGRESOS_BBVA: dict = {
    HeaderBBVA.FECHA: Utf8,  # O Date si quieres tipo fecha directamente
    HeaderBBVA.REG: Utf8,
    HeaderBBVA.REFERENCIA: Utf8,
    HeaderBBVA.DESCRIPCION: Utf8,
    HeaderBBVA.MONTO: Decimal(12, 2),
    HeaderBBVA.ESTADO: Utf8,
    HeaderBBVA.COMENTARIO: Utf8,
    HeaderBBVA.GLOSA: Utf8,
}
SCHEMA_INGRESOS_BBVA: dict = {
    HeaderBBVAING.FECHA: Utf8,
    HeaderBBVAING.REFERENCIA: Utf8,
    HeaderBBVAING.DESCRIPCION: Utf8,
    HeaderBBVAING.METODO: Utf8,
    HeaderBBVAING.MONTO: Decimal(12, 2),
}
SCHEMA_INGRESOS_BCP: dict = {
    HeaderBCPING.FECHA: Utf8,
    HeaderBCPING.REFERENCIA: Utf8,
    HeaderBCPING.DESCRIPCION: Utf8,
    HeaderBCPING.METODO: Utf8,
    HeaderBCPING.MONTO: Decimal(12, 2),
}
SCHEMA_INGRESOS_IBK: dict = {
    HeaderIBKING.FECHA: Utf8,
    HeaderIBKING.REFERENCIA: Utf8,
    HeaderIBKING.DESCRIPCION: Utf8,
    HeaderIBKING.METODO: Utf8,
    HeaderIBKING.MONTO: Decimal(12, 2),
}
SCHEMA_INGRESOS_SKB: dict = {
    HeaderSKBING.FECHA: Utf8,
    HeaderSKBING.REFERENCIA: Utf8,
    HeaderSKBING.DESCRIPCION: Utf8,
    HeaderSKBING.METODO: Utf8,
    HeaderSKBING.MONTO: Decimal(12, 2),
}
