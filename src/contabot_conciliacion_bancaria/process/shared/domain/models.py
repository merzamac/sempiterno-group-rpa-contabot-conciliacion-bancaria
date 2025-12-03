from pathlib import Path
from dataclasses import dataclass
from typing import Any
from datetime import date
from polars import DataFrame
from contabot_conciliacion_bancaria.types import SuffixTypes
from abc import ABC, abstractmethod
from dataclasses import dataclass
from openpyxl import Workbook


class Row(ABC):
    """Clase abstracta base para todas las filas"""

    @abstractmethod
    def __getitem__(self, key: str) -> Any:
        """Permite acceso como row['nombre_columna']"""
        pass

    @abstractmethod
    def __setitem__(self, key: str, value: Any):
        """Permite modificación como row['nombre_columna'] = value"""
        pass


@dataclass
class FileToUpload:
    file_Path: Path
    type_transaction: str
    date: date


class Child:

    def __init__(
        self, name: Path, wb: Workbook, suffix: SuffixTypes, to_upload: bool
    ) -> None:
        self.name = name
        self.wb = wb
        self.suffix: SuffixTypes = suffix
        self.file_name: str = f"{self.name}{suffix.value}"
        self.to_upload: bool = to_upload

    def save(self, save_dir: Path) -> FileToUpload | None:
        # save_dir.mkdir(parents=True, exist_ok=True)
        file_path: Path = save_dir / self.file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if self.suffix.value == SuffixTypes.XLSX.value:
            self.wb.save(f"{file_path}")

        if self.suffix.value == SuffixTypes.CSV.value:
            self.wb.save(f"{file_path}")
        if self.to_upload:
            return FileToUpload(
                file_Path=file_path, type_transaction="", date=date.today()
            )
        return None


@dataclass
class RowMovement(Row):
    """Fila para transacciones financieras movimientos"""

    fecha_pagos: date
    referencia: str
    descripcion: str
    # movimiento: str
    tipo_transaccion: str
    monto: float
    estado: str
    tipo_moneda: str
    glosa: str
    pagos: str

    banco: str

    def __getitem__(self, key: str):
        """Permite acceso como row['fecha']"""
        return getattr(self, key)

    def __setitem__(self, key: str, value):
        """Permite modificación como row['fecha'] = value"""
        setattr(self, key, value)

    def __iter__(self):
        """Permite conversion a tuple: tuple(row)"""
        return iter(
            [
                "",
                self.fecha_pagos,
                self.referencia,
                self.descripcion,
                self.monto,
                self.estado or "",
                "",
                self.glosa,
            ]
        )

    def __len__(self):
        """Define la longitud del objeto"""
        return len(self.__dataclass_fields__)


@dataclass
class RowReport(Row):
    """Fila para transacciones financieras reporte"""

    fecha_emision: date
    tipo: str
    concatenar: str
    ser_doc: str
    numero_doc: str
    ruc: str
    razon_social: str
    glosa: str
    tipo_moneda: str
    monto: float
    banco: str
    pagos: str
    fecha_pagos: date

    def __getitem__(self, key: str):
        """Permite acceso como row['fecha']"""
        return getattr(self, key)

    def __setitem__(self, key: str, value):
        """Permite modificación como row['fecha'] = value"""
        setattr(self, key, value)


@dataclass
class RowMasivo(Row):

    anio: str
    mes: str
    num_compbte: str
    items: str
    cen_costo: str
    cta_contable: str
    cod_dcto: str
    num_dcto: str
    cod_cliente: str
    fch_dcto: date
    fch_vto: date
    glosa: str
    mon: str
    tip_mvto: str
    valor_mn: str
    valor_me: str

    def __getitem__(self, key: str):
        """Permite acceso como row['fecha']"""
        return getattr(self, key)

    def __setitem__(self, key: str, value):
        """Permite modificación como row['fecha'] = value"""
        setattr(self, key, value)

    def __iter__(self):
        """Permite conversion a tuple: tuple(row)"""
        return iter(
            [
                self.anio,
                self.mes,
                self.num_compbte,
                self.items,
                self.cen_costo,
                self.cta_contable,
                self.cod_dcto,
                self.num_dcto,
                self.cod_cliente,
                self.fch_dcto.strftime("%d/%m/%Y"),
                self.fch_vto.strftime("%d/%m/%Y"),
                self.glosa,
                self.mon,
                self.tip_mvto,
                self.valor_mn,
                self.valor_me,
            ]
        )
