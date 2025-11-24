# movimientos/comparators.py
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


class MontoComparator:
    @staticmethod
    def coinciden(
        rows_report: tuple, movements, index_list: list, masivo: list[RowMovement]
    ) -> bool:
        """Compara si los montos coinciden"""
        monto_reporte = round(sum([row.monto for row in rows_report]), 2)
        # bank = rows_report[0].banco
        # moneda = rows_report[0].tipo_moneda
        for index, row in enumerate(movements, 2):
            if row.tipo_moneda == Moneda.USD:
                # COMISIONES DE BANCOS EN DOLARES
                with_comision25 = abs(monto_reporte) + 25
                with_comision20 = abs(monto_reporte) + 20
                with_comision5 = abs(monto_reporte) + 5

                monto_encontrado = (
                    abs(row.monto) == abs(monto_reporte)
                    or abs(row.monto) == with_comision25  # comision para sbk
                    or abs(row.monto) == with_comision20  # comision para ibk
                    or abs(row.monto) == with_comision5
                )
                if monto_encontrado:
                    index_list.append(index)
                    row.glosa = f"PG {rows_report[0].pagos}"
                    masivo.append(row)
                    return monto_encontrado
            if row.tipo_moneda == Moneda.PEN:
                # COMISIONES DE BANCOS EN SOLES
                with_comision5 = abs(monto_reporte) + 5
                monto_encontrado = abs(monto_reporte) == abs(row.monto) or abs(
                    monto_reporte
                ) == (
                    with_comision5
                )  # comision para ibk
                if monto_encontrado:
                    index_list.append(index)
                    row.glosa = f"PG {rows_report[0].pagos}"

                    masivo.append(row)
                    return monto_encontrado

        combinados = filter_with_combinations_movimientos(movements)
        for to_conciliar in combinados:
            encontrar_coincidencias = tuple(
                (movement, index)
                for index, movement in enumerate(movements, 2)
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
