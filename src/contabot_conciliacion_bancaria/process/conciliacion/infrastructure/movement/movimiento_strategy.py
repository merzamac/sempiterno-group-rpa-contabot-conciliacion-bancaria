# movimientos/__init__.py
from contabot_conciliacion_bancaria.process.conciliacion.infrastructure.movement.comparators import (
    MontoComparatorReports,
)
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from .comparators import (
    ReporteComparator,
    MontoComparatorReports,
    MontoComparatorMovements,
)
from contabot_conciliacion_bancaria.process.conciliacion.types import (
    ReportToConciliar,
    ToConciliar,
)
from contabot_conciliacion_bancaria.process.shared.domain.models import RowMovement


# Strategy Pattern
class MovimientoStrategy(ABC):
    @abstractmethod
    def procesar(self, movements: tuple, data_to_conciliar: ReportToConciliar) -> Dict:
        pass


# Concrete Strategies
class IngresosStrategy(MovimientoStrategy): ...


class EgresosStrategy(MovimientoStrategy):
    def procesar(self, movements: tuple, data_to_conciliar: ReportToConciliar) -> Dict:
        coincidencias: list = []
        masivo: list[RowMovement] = []
        for glosa_data in data_to_conciliar.glosas:
            # for index, row in enumerate(movement, 2):
            # if glosa_data.glosa == "PROV EXT SOFTPLAN":
            #     print(glosa_data.glosa)  # and fecha_emision == row.fecha_emision:
            rows_report, marcar_glosa_con_fecha = (
                ReporteComparator.encontrar_coincidencias(
                    glosa_data, data_to_conciliar.report
                )
            )
            # devuelve las filas de reportes que tienen la misma glosa y fecha

            if rows_report and not MontoComparatorReports.coinciden(
                rows_report, movements, coincidencias, masivo
            ):
                MontoComparatorMovements.coinciden(
                    rows_report, movements, coincidencias, masivo
                )
                ##values = coincidencias[-1]

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
