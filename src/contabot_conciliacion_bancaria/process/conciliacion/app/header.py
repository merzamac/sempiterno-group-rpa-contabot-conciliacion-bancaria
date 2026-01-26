from enum import StrEnum
from abc import ABC, abstractmethod, ABCMeta


class Header(StrEnum):
    @abstractmethod
    def values(self): ...


class HeaderReport(StrEnum):
    FECHA_EMISION = "FECHA EMISIÓN"
    TIPO = "TIPO"
    CONCATENAR = "CONCATENAR"
    SER_DOC = "SER. DOC."
    NUM_DOC = "NUM. DOC."
    RUC = "RUC"
    NOMBRE_RAZON_SOCIAL = "NOMBRE O RAZON SOCIAL"
    GLOSA = "GLOSA"
    MONEDA = "MON"
    TOTAL = "TOTAL"
    BANCO = "BANCO"
    PAGOS = "PAGOS"
    FECHA_PAGO = "FECHA DE PAGO"
    REGISTRO = "REGISTRO"
    COMENTARIO = "COMENTARIO"


class HeaderBCP(Header):
    REG = "REG"
    FECHA = "Fecha"
    REFERENCIA = "Operación - Número"
    DESCRIPCION = "Descripción operación"
    MONTO = "Monto"
    ESTADO = "ESTADO"
    COMENTARIO = "COMENTARIO"
    GLOSA = "GLOSA"

    @classmethod
    def values(cls):
        return (
            cls.REG.value,
            cls.FECHA.value,
            cls.REFERENCIA.value,
            cls.DESCRIPCION.value,
            cls.MONTO.value,
            cls.ESTADO.value,
            cls.COMENTARIO.value,
            cls.GLOSA.value,
        )


class HeaderSBK(Header):
    REG = "REG"
    FECHA = "Fecha"
    REFERENCIA = "Referencia"
    DESCRIPCION = "Movimiento"
    MONTO = "Importe"
    ESTADO = "ESTADO"
    COMENTARIO = "COMENTARIO"
    GLOSA = "GLOSA"

    @classmethod
    def values(cls):
        return (
            cls.REG.value,
            cls.FECHA.value,
            cls.REFERENCIA.value,
            cls.DESCRIPCION.value,
            cls.MONTO.value,
            cls.ESTADO.value,
            cls.COMENTARIO.value,
            cls.GLOSA.value,
        )


class HeaderIBK(Header):
    REG = "REG"
    FECHA = "Fecha de operación"
    REFERENCIA = "Nro. de operación"
    DESCRIPCION = "Movimiento"
    MOVIMIENTO = "Descripción"
    MONTO = "Cargo"
    ESTADO = "ESTADO"
    COMENTARIO = "COMENTARIO"
    GLOSA = "GLOSA"

    @classmethod
    def values(cls):
        return (
            cls.REG.value,
            cls.FECHA.value,
            cls.REFERENCIA.value,
            cls.DESCRIPCION.value,
            cls.MONTO.value,
            cls.ESTADO.value,
            cls.COMENTARIO.value,
            cls.GLOSA.value,
        )


class HeaderBBVA(Header):
    REG = "REG"
    FECHA = "F. Operación"
    REFERENCIA = "Nº. Doc."
    DESCRIPCION = "Concepto"
    MONTO = "Importe"
    ESTADO = "ESTADO"
    COMENTARIO = "COMENTARIO"
    GLOSA = "GLOSA"

    @classmethod
    def values(cls):
        return (
            cls.REG.value,
            cls.FECHA.value,
            cls.REFERENCIA.value,
            cls.DESCRIPCION.value,
            cls.MONTO.value,
            cls.ESTADO.value,
            cls.COMENTARIO.value,
            cls.GLOSA.value,
        )


class HeaderMasivo(Header):
    """Header para el formato de carga masiva contable"""

    ANIO = "AÑO"
    MES = "MES"
    REGISTRO = "NUM_COMPBTE"
    ITEMS = "ITEMS"
    CEN_COSTO = "CEN_COSTO"
    CTA_CONTABLE = "CTA_CONTABLE"
    COD_DCTO = "COD_DCTO"
    NUM_DCTO = "NUM_DCTO"
    COD_CLIENTE = "COD_CLIENTE"
    FCH_DCTO = "FCH_DCTO"
    FCH_VTO = "FCH_VTO"
    GLOSA = "GLOSA"
    MON = "MON"
    TIP_MVTO = "TIP_MVTO"
    VALOR_MN = "VALOR_MN"
    VALOR_ME = "VALOR_ME"

    @classmethod
    def values(cls):
        return (
            cls.ANIO.value,
            cls.MES.value,
            cls.REGISTRO.value,
            cls.ITEMS.value,
            cls.CEN_COSTO.value,
            cls.CTA_CONTABLE.value,
            cls.COD_DCTO.value,
            cls.NUM_DCTO.value,
            cls.COD_CLIENTE.value,
            cls.FCH_DCTO.value,
            cls.FCH_VTO.value,
            cls.GLOSA.value,
            cls.MON.value,
            cls.TIP_MVTO.value,
            cls.VALOR_MN.value,
            cls.VALOR_ME.value,
        )


class HeaderBCPING(Header):
    FECHA = "Fecha"
    REFERENCIA = "Operación - Número"
    DESCRIPCION = "Descripción operación"
    METODO = "XXX"
    MONTO = "Monto"
    # SALDO = "Saldo"
    # SUCURSAL = "Sucursal - agencia"


class HeaderSKBING(Header):
    FECHA = "Fecha"
    REFERENCIA = "Referencia"
    DESCRIPCION = "Movimiento"
    METODO = "XXX"
    MONTO = "Importe"


class HeaderIBKING(Header):
    FECHA = "Fecha de operación"
    REFERENCIA = "Nro. de operación"
    DESCRIPCION = "Movimiento"
    METODO = "XXX"
    MONTO = "Abono"


class HeaderBBVAING(Header):
    FECHA = "F. Operación"
    REFERENCIA = "Nº. Doc."
    DESCRIPCION = "Concepto"
    METODO = "XXX"
    MONTO = "Importe"
