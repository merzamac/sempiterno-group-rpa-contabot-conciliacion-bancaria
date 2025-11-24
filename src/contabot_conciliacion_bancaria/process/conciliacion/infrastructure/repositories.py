from pathlib import Path
from datetime import date

from contabot_conciliacion_bancaria.process.conciliacion.infrastructure.movement.excel_builder import (
    ReportExcelBuilder,
)
from contabot_conciliacion_bancaria.process.conciliacion.infrastructure.movement.context import (
    GetReport,
    MasivoByBank,
    DuplicateMasivo,
    MasivoByDate,
    MasivoIngresosByBank,
)
from contabot_conciliacion_bancaria.paths import (
    EGR_PEN_DIR,
    EGR_USD_DIR,
    MASIVOS_INGRESOS_DIR,
)
from contabot_conciliacion_bancaria.process.conciliacion.infrastructure.movement.masivo import (
    Masivo,
)
from contabot_conciliacion_bancaria.process.shared.app.use_cases import (
    ExtractInsideDirectory,
)
from contabot_conciliacion_bancaria.process.shared.domain.repositories import Container
from contabot_conciliacion_bancaria.process.conciliacion.types import ConciliacionFiles
from contabot_conciliacion_bancaria.process.conciliacion.app.uses_case import (
    GetFormatedToConciliar,
    GetFormatedEgresosMovement,
    GetFormatedIngresosMovement,
)
from contabot_conciliacion_bancaria.types import SuffixTypes
from contabot_conciliacion_bancaria.process.shared.domain.models import Child


class ConciliacionContainer(Container):
    def __init__(self, file_path: Path) -> None:
        # files: dict[str, Path] = ExtractInsideDirectory.execute(file_path, 2)
        reports, movements = ExtractInsideDirectory.execute(file_path, 2)
        self.files: ConciliacionFiles = ConciliacionFiles(
            movement=movements, report=reports
        )
        self.excel_builder = ReportExcelBuilder()
        self.masivo_egresos: Masivo
        self.masivo_ingresos: Masivo

    def conciliar(self) -> None:
        masivo_list: list[type] = []
        egresos_soles, egresos_dolares = GetFormatedEgresosMovement.execute(
            excel_path=self.files.movement
        )
        ingresos_soles, ingresos_dolares = GetFormatedIngresosMovement.execute(
            excel_path=self.files.movement
        )
        conciliar = GetFormatedToConciliar.execute(excel_path=self.files.report)
        GetReport.execute(
            conciliar,
            egresos_soles,
            self.excel_builder,
            masivo_list,
        )
        GetReport.execute(
            conciliar,
            egresos_dolares,
            self.excel_builder,
            masivo_list,
        )

        self.masivo_egresos = Masivo(tuple(masivo_list))
        self.masivo_ingresos = Masivo(tuple(ingresos_soles))
        self.pack_to_save: list[Child] = [
            Child(
                Path("Movimientos"),
                self.excel_builder.build(),
                SuffixTypes.XLSX,
            ),
        ]

    def masivo(self, period_date: date) -> None:
        # masivo_egresos_dir = Path("MASIVO EGRESOS")
        # masivo_ingresos_dir = Path("MASIVO EGRESOS")
        # pen_dir = masivo_egresos_dir / "SOLES"
        # usd_dir = masivo_egresos_dir / "DOLARES"
        by_pen = self.masivo_egresos.soles_by_bank()
        by_usd = self.masivo_egresos.dolares_by_bank()
        ingresos_by_bank = self.masivo_ingresos.ingresos_pen_by_bank()
        MasivoIngresosByBank.execute(ingresos_by_bank, MASIVOS_INGRESOS_DIR, self.pack_to_save)
        for name_sheet, report in by_pen.items():
            by_pen[name_sheet] = DuplicateMasivo.execute(list(report))
        for name_sheet, report in by_usd.items():
            by_usd[name_sheet] = DuplicateMasivo.execute(list(report))

        # se obtien los masivos de los bancos
        MasivoByBank.execute(by_pen, EGR_PEN_DIR, self.pack_to_save)
        MasivoByBank.execute(by_usd, EGR_USD_DIR, self.pack_to_save)
        MasivoByDate.execute(by_pen, EGR_PEN_DIR, self.pack_to_save, period_date)
        MasivoByDate.execute(by_pen, EGR_USD_DIR, self.pack_to_save, period_date)

        self.children = tuple(self.pack_to_save)
