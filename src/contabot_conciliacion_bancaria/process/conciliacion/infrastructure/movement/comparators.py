# movimientos/comparators.py
from abc import ABC, abstractmethod


class ReporteComparator(ABC):
    @staticmethod
    def encontrar_coincidencias(glosa: str, reportes: tuple) -> list:
        """Encuentra reportes que coincidan con el movimiento"""
        coincidencias = []
        for reporte in reportes:
            if reporte.pagos == glosa:
                coincidencias.append(reporte)
        return coincidencias


class MontoComparator:
    @staticmethod
    def coinciden(rows_report: list, movimiento) -> bool:
        """Compara si los montos coinciden"""
        monto_reporte = sum([row.monto for row in rows_report])
        monto_movimiento = movimiento.monto
        return abs(monto_reporte) == abs(monto_movimiento)
