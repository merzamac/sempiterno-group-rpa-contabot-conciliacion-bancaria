from datetime import datetime, date

from contabot_conciliacion_bancaria.process.constants import (
    PAYMENT_GATEWAYS_POSIBILITES,
)
from contabot_conciliacion_bancaria.process.constants import MONEDAS, BANKS
from contabot_conciliacion_bancaria.process.shared.domain.models import RowMasivo
from contabot_conciliacion_bancaria.process.conciliacion.app.cuenta_contable import (
    CuentaContable,
    Moneda,
    Bank,
    PaymentGateway,
)
from contabot_conciliacion_bancaria.utils.filter import search


class Masivo:
    def __init__(self, masivo: tuple) -> None:
        self.usd = tuple(r for r in masivo if r.tipo_moneda == Moneda.USD.value)
        self.pen = tuple(r for r in masivo if r.tipo_moneda == Moneda.PEN.value)

    def generic_data(self, moneda: str, date: date) -> dict:
        today = date.today()
        anio = str(today.year)
        mes = str(today.month).zfill(2)
        return {
            "anio": anio,
            "mes": mes,
            "item": "001",
            "cen_costo": "",
            "cod_dcto": "00",
            "cod_cliente": "",
            "mon": moneda,
            "tip_mvto": "A",
            "valor_me": "0",
        }

    def soles_by_bank(self, date: date) -> dict:
        moneda = "N"
        return self._by_bank(
            reports=self.pen,
            generic_data=self.generic_data(moneda, date),
        )

    def ingresos_pen_by_bank(self, date: date) -> dict:
        # values = tuple(r for r in self.pen if r.tipo_transaccion == "")
        # con la linea comentada puedes ver cueantas movimientos llegan con tipo de transaccion vacio
        # citiban no se considera para los ingresos
        return self._by_bank_and_payment(
            reports=self.pen,
            generic_data=self.generic_data(Moneda.PEN.type(), date),
        )

    def dolares_by_bank(self, date: date) -> dict:

        return self._by_bank(
            self.usd, generic_data=self.generic_data(Moneda.USD.type(), date)
        )

    def _by_bank(self, reports: tuple, generic_data: dict) -> dict:
        by_bank: dict = {}
        for bank in Bank:
            bank_reports = [report for report in reports if report.banco == bank.value]
            by_bank[bank.value] = tuple(
                self._parse_masivo(generic_data, index, report)
                for index, report in enumerate(bank_reports, 1)
            )
        return by_bank

    def _by_bank_and_payment(self, reports: tuple, generic_data: dict) -> dict:
        by_bank_and_payment: dict = {}
        posibilities = (
            tuple(member.value for member in PaymentGateway.__members__.values())
            + PAYMENT_GATEWAYS_POSIBILITES
        )
        for bank in Bank:
            bank_reports = [
                report
                for report in reports
                if report.banco == bank.value
                and report.tipo_transaccion in posibilities
            ]
            for payment in PaymentGateway:
                bank_reports_by_payment = [
                    report
                    for report in bank_reports
                    if report.tipo_transaccion.endswith(payment.value)
                ]
                by_bank_and_payment[f"{payment.value} {bank.value}"] = tuple(
                    self._parse_masivo(generic_data, index, report)
                    for index, report in enumerate(bank_reports_by_payment, 1)
                )
        return by_bank_and_payment

    # {
    #     bank: tuple(
    #         self._parse_masivo(generic_data, index, report)
    #         for index, report in enumerate(reports, 1)
    #         if report.banco == bank
    #     )
    #     for bank in BANKS
    # }

    @classmethod
    def _parse_masivo(self, data: dict, index_: int, report) -> RowMasivo:
        index = str(index_).zfill(2)
        # 104132 ibk
        # 104114 sbk
        # 104141 bbva
        # 104121 bcp
        cta_contable = {
            "IBK": "104132",
            "SBK": "104114",
            "BBVA": "104141",
            "BCP": "104121",
        }

        return RowMasivo(
            anio=data["anio"],
            mes=data["mes"],
            num_compbte=index,
            items=data["item"],
            cen_costo=data["cen_costo"],
            cta_contable=str(
                CuentaContable().cuenta(report.banco, Moneda[report.tipo_moneda])
            ),
            cod_dcto=data["cod_dcto"],
            num_dcto=report.referencia,
            cod_cliente=data["cod_cliente"],
            fch_dcto=report.fecha_pagos,
            fch_vto=report.fecha_pagos,
            glosa=report.glosa,
            mon=data["mon"],
            tip_mvto=data["tip_mvto"],
            valor_mn=abs(report.monto),
            valor_me=data["valor_me"],
        )


class MasivoReport:
    def by_bank(self) -> None:
        pass

    def by_date(self) -> None:
        pass
