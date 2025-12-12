from contabot_conciliacion_bancaria.process.constants import BANKS
from contabot_conciliacion_bancaria.process.conciliacion.types import ToConciliar
import difflib

from contabot_conciliacion_bancaria.process.conciliacion.app.comisiones import Comision


def filter_with_combinations(reports: tuple, resultados: list) -> None:
    """
    Filtra los reportes para encontrar combinaciones de pagos y fechas que no se han visto antes.

    Parameters:
    reports (tuple): Los reportes que se van a conciliar.
    resultados (list): La lista donde se guardan los resultados.

    Returns:
    list: La lista de resultados con las combinaciones de pagos y fechas que no se han visto antes.
    """
    for bank in BANKS:
        combinaciones_vistas = set()
        reports_by_bank = [r for r in reports if r.banco == bank]
        for report in reports_by_bank:
            combinacion = (report.pagos, report.fecha_pagos)
            if combinacion not in combinaciones_vistas:
                combinaciones_vistas.add(combinacion)
                resultados.append(
                    ToConciliar(glosa=report.pagos, fecha=report.fecha_pagos)
                )


def filter_with_combinations_movimientos(movements: tuple) -> tuple:
    resultados: list = []
    combinaciones_vistas = set()
    for movement in movements:
        combinacion = (movement.pagos, movement.fecha_pagos)
        if combinacion not in combinaciones_vistas:
            combinaciones_vistas.add(combinacion)
            resultados.append(
                ToConciliar(glosa=movement.pagos, fecha=movement.fecha_pagos)
            )

    return tuple(resultados)


def search(words: str, posibilities: tuple, cutoff: float = 0.6) -> str:

    for word in words.replace(".", " ").split():
        concidences = difflib.get_close_matches(
            word=word.upper(), possibilities=posibilities, n=1, cutoff=cutoff
        )
        if concidences:
            return str(concidences[0])
    return ""


def found_amount(amount_movement: float, amount_report: float) -> bool:
    return (
        abs(amount_movement) == abs(amount_report)
        or abs(amount_movement)
        == abs(Comision.con_25(amount_report))  # comision para sbk
        or abs(amount_movement)
        == abs(Comision.con_20(amount_report))  # comision para ibk
        or abs(amount_movement) == abs(Comision.con_5(amount_report))
        or abs(amount_movement) == abs(Comision.con_1_71(amount_report))
    )
