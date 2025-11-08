from polars import col, Expr


def safe_date_col(column_names: list) -> Expr:
    """Crea una expresión de fecha que maneja columnas opcionales de forma segura"""

    return (
        col(column_names)
        .str.to_datetime("%Y-%m-%d %H:%M:%S", strict=False)
        .fill_null(col(column_names).str.to_datetime("%Y-%m-%d", strict=False))
        .fill_null(col(column_names).str.to_datetime("%d/%m/%Y", strict=False))
    )


# Uso
# DATE_COL = safe_date_col(HeaderReport.FECHA_EMISION, HeaderReport.FECHA_PAGO)
