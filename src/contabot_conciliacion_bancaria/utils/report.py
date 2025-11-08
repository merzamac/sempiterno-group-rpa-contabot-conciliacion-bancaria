from datetime import date


def get_rows_report(glosa: str, fecha_emision: date, report: tuple) -> list:
    rows_report: list = []
    for row in report:
        if glosa == row.pagos:  # and fecha_emision == row.fecha_emision:
            rows_report.append(row)

    return rows_report
