# movimientos/__init__.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from .comparators import ReporteComparator, MontoComparator


# Strategy Pattern
class MovimientoStrategy(ABC):
    @abstractmethod
    def procesar(self, movimientos: tuple, reportes: tuple) -> Dict:
        pass


# Concrete Strategies
class IngresosStrategy(MovimientoStrategy): ...


class EgresosStrategy(MovimientoStrategy):
    def procesar(self, movement: tuple, reportes: tuple) -> Dict:
        coincidencias = []
        masivo = []

        for index, row in enumerate(movement, 2):
            rows_report = ReporteComparator.encontrar_coincidencias(row.glosa, reportes)
            if rows_report and MontoComparator.coinciden(rows_report, row):
                coincidencias.append(index)
                masivo.extend(rows_report)

        return {
            "coincidencias": coincidencias,
            "masivo": masivo,
        }


# Factory Pattern
# class MovimientoStrategyFactory:
#     @staticmethod
#     def create_strategy(tipo_movimiento: str) -> MovimientoStrategy:
#         strategies = {
#             "ingresos": IngresosStrategy,
#             "egresos": EgresosStrategy,
#             # "transferencias": TransferenciasStrategy,
#         }

#         strategy_class = strategies.get(tipo_movimiento.lower())
#         if not strategy_class:
#             raise ValueError(f"Tipo de movimiento no soportado: {tipo_movimiento}")

#         return strategy_class()
