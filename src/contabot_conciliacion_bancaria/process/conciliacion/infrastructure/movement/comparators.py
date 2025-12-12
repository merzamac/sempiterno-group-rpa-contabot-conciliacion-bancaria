# movimientos/comparators.py
from contabot_conciliacion_bancaria.utils.filter import found_amount
from abc import ABC, abstractmethod
from contabot_conciliacion_bancaria.process.conciliacion.app.cuenta_contable import (
    Moneda,
)
from contabot_conciliacion_bancaria.process.conciliacion.types import (
    ReportToConciliar,
    ToConciliar,
)
from contabot_conciliacion_bancaria.process.constants import BANKS, MONEDAS
from contabot_conciliacion_bancaria.process.shared.domain.models import RowMovement
from contabot_conciliacion_bancaria.utils.filter import (
    filter_with_combinations_movimientos,
)

from contabot_conciliacion_bancaria.process.conciliacion.app.comisiones import Comision


class ReporteComparator(ABC):
    @staticmethod
    def encontrar_coincidencias(glosa: ToConciliar, reportes: tuple) -> tuple:
        """Encuentra reportes que coincidan con el movimiento"""
        coincidencias = []
        marcar_glosa_con_fecha = False
        for reporte in reportes:
            if reporte.pagos == glosa.glosa and reporte.fecha_pagos == glosa.fecha:
                coincidencias.append(reporte)
            if (
                reporte.pagos == glosa.glosa
                and reporte.fecha_pagos != glosa.fecha
                and not marcar_glosa_con_fecha
            ):
                marcar_glosa_con_fecha = True

        return tuple(coincidencias), marcar_glosa_con_fecha


class MontoComparatorReports:
    @staticmethod
    def coinciden(
        rows_report: tuple, movements, index_list: list, masivo: list[RowMovement]
    ) -> bool:
        """Compara si los montos coinciden"""
        monto_reporte: float = round(sum([row.monto for row in rows_report]), 2)
        # bank = rows_report[0].banco
        # moneda = rows_report[0].tipo_moneda
        start: int = 2  # comenzamos desde 2, porque la 1 ya es el header para el excel

        for index, row in enumerate(movements, start):
            if row.tipo_moneda == Moneda.USD:
                monto_encontrado = found_amount(row.monto, monto_reporte)
                if monto_encontrado:
                    index_list.append(index)
                    row.glosa = f"PG {rows_report[0].pagos}"
                    masivo.append(row)

                    return monto_encontrado
            if row.tipo_moneda == Moneda.PEN:
                # COMISIONES DE BANCOS EN SOLES
                monto_encontrado = found_amount(row.monto, monto_reporte)
                if monto_encontrado:
                    index_list.append(index)
                    row.glosa = f"PG {rows_report[0].pagos}"

                    masivo.append(row)
                    ##del movements[index - 2]
                    return monto_encontrado
        return False


class MontoComparatorMovements:
    @staticmethod
    def coinciden(
        rows_report: tuple, movements, index_list: list, masivo: list[RowMovement]
    ) -> bool:
        monto_reporte = round(sum([row.monto for row in rows_report]), 2)
        combinados = filter_with_combinations_movimientos(movements)
        start: int = 2  # comenzamos desde 2, porque la 1 ya es el header para el excel
        for to_conciliar in combinados:
            encontrar_coincidencias = tuple(
                (movement, index)
                for index, movement in enumerate(movements, start)
                if movement.pagos == to_conciliar.glosa
                and movement.fecha_pagos == to_conciliar.fecha
            )
            monto = round(
                sum(
                    (movimiento.monto for movimiento, index in encontrar_coincidencias)
                ),
                2,
            )
            monto_encontrado = abs(monto) == abs(monto_reporte)
            if monto_encontrado:
                for movimiento, index in encontrar_coincidencias:
                    index_list.append(index)
                    movimiento.glosa = f"PG {rows_report[0].pagos}"
                    masivo.append(movimiento)

                return monto_encontrado

        return False
