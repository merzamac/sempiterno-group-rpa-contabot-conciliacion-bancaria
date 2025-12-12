class Comision:
    @staticmethod
    def con_25(monto_reporte: float) -> float:
        return monto_reporte + 25

    @staticmethod
    def con_20(monto_reporte: float) -> float:
        return monto_reporte + 20

    @staticmethod
    def con_5(monto_reporte: float) -> float:
        return monto_reporte + 5

    @staticmethod
    def con_1_71(monto_reporte: float) -> float:
        return monto_reporte + 1.71

    @staticmethod
    def calcular(monto_reporte: float, valor_comision: int) -> float:
        return monto_reporte + valor_comision
