from datetime import datetime, date
from contabot_conciliacion_bancaria.process.constants import MONEDAS, BANKS
from contabot_conciliacion_bancaria.process.shared.domain.models import RowMasivo


class Masivo:
    def __init__(self, masivo: tuple) -> None:
        self.usd = tuple(r for r in masivo if r.tipo_moneda == MONEDAS["USD"])
        self.pen = tuple(r for r in masivo if r.tipo_moneda == MONEDAS["PEN"])

    def generic_data(self, moneda: str) -> dict:
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

    def soles_by_bank(self) -> dict:
        moneda = "N"
        return self._by_bank(
            reports=self.pen,
            generic_data=self.generic_data(moneda),
        )

    def dolares_by_bank(self) -> dict:
        moneda = "E"
        return self._by_bank(self.usd, generic_data=self.generic_data(moneda))

    def _by_bank(self, reports: tuple, generic_data: dict) -> dict:
        by_bank: dict = {}
        for bank in BANKS:
            bank_reports = [report for report in reports if report.banco == bank]
            by_bank[bank] = tuple(
                self._parse_masivo(generic_data, index, report)
                for index, report in enumerate(bank_reports, 1)
            )
        return by_bank

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
            cta_contable=cta_contable[report.banco],
            cod_dcto=data["cod_dcto"],
            num_dcto=report.numero_doc,
            cod_cliente=data["cod_cliente"],
            fch_dcto=report.fecha_emision,
            fch_vto=report.fecha_emision,
            glosa=report.glosa,
            mon=data["mon"],
            tip_mvto=data["tip_mvto"],
            valor_mn=report.monto,
            valor_me=data["valor_me"],
        )


class MasivoReport:
    def by_bank(self) -> None:
        pass

    def by_date(self) -> None:
        pass
