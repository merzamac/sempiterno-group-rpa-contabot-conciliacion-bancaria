class Comision:
    def __init__(self):
        self.COMISION_25 = 25
        self.COMISION_20 = 20
        self.COMISION_5 = 5
        self.SIN_COMISION = 0

    def con_25(self, monto_reporte: float) -> float:
        return monto_reporte + self.COMISION_25

    def con_20(self, monto_reporte: float) -> float:
        return monto_reporte + self.COMISION_20

    def con_5(self, monto_reporte: float) -> float:
        return monto_reporte + self.COMISION_5

    def sin_comision(self, monto_reporte: float) -> float:
        return monto_reporte + self.SIN_COMISION

    def calcular(self, monto_reporte: float, valor_comision: int) -> float:
        return monto_reporte + valor_comision
