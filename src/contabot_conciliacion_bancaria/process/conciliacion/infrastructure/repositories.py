from pathlib import Path
from datetime import date
import calendar

from polars import last

# from openpyxl.utils import column_index_from_string, get_column_letter
# from contabot_conciliacion_bancaria.process.conciliacion.infrastructure.movement.context import ( ProcesadorMovimientos,)
from contabot_conciliacion_bancaria.process.conciliacion.infrastructure.movement import (
    masivo,
)
from contabot_conciliacion_bancaria.process.conciliacion.infrastructure.movement.excel_builder import (
    ReportExcelBuilder,
    MasivoExcelBuilder,
)
from contabot_conciliacion_bancaria.process.conciliacion.infrastructure.movement.context import (
    GetReport,
    MasivoByBank,
    DuplicateMasivo,
    MasivoByDate,
)
from contabot_conciliacion_bancaria.process.conciliacion.infrastructure.movement.movimiento_strategy import (
    EgresosStrategy,
)
from contabot_conciliacion_bancaria.process.conciliacion.infrastructure.movement.masivo import (
    Masivo,
)
from contabot_conciliacion_bancaria.utils.report import get_rows_report
from contabot_conciliacion_bancaria.process.shared.app.use_cases import (
    ExtractInsideDirectory,
)
from contabot_conciliacion_bancaria.process.shared.domain.repositories import Container
from contabot_conciliacion_bancaria.process.conciliacion.types import ConciliacionFiles
from contabot_conciliacion_bancaria.process.conciliacion.app.uses_case import (
    GetFormatedReports,
    GetFormatedMovements,
)
from contabot_conciliacion_bancaria.process.conciliacion.app.uses_case import (
    ExtractConciliacionFiles,
)
from contabot_conciliacion_bancaria.types import SuffixTypes, FileType
from contabot_conciliacion_bancaria.process.shared.domain.models import Child


class ConciliacionContainer(Container):
    def __init__(self, file_path: Path) -> None:
        # files: dict[str, Path] = ExtractInsideDirectory.execute(file_path, 2)
        self.files: ConciliacionFiles = ExtractConciliacionFiles.execute(
            ExtractInsideDirectory.execute(file_path, 2)
        )
        self.excel_builder = ReportExcelBuilder()
        self.masivo_list: Masivo

        # self.reportes = GetFormatedReports.execute(excel_path=result["reportes"])
        # GetReport.execute(
        #     GetFormatedReports.execute(excel_path=result["reportes"]),
        #     GetFormatedMovements.execute(excel_path=result["movimientos"])[0],
        #     self.excel_builder,
        #     masivo,
        # )
        # GetReport.execute(
        #     GetFormatedReports.execute(excel_path=result["reportes"]),
        #     GetFormatedMovements.execute(excel_path=result["movimientos"])[1],
        #     self.excel_builder,
        #     masivo,
        # )
        # self.movements = GetFormatedMovements.execute(excel_path=result["movimientos"])
        # children: list[Child] = []

    def conciliar(self) -> None:

        # movements_pen, movements_usd = self.movements
        # masivo: list[type] = []
        # GetReport.execute(movements_pen, self.reportes, masivo, self.excel_builder)
        # GetReport.execute(movements_usd, self.reportes, masivo, self.excel_builder)

        # self.masivo = Masivo(tuple(masivo))
        reports = self.files["reportes"]
        movements = self.files["movimientos"]
        masivo_list: list[type] = []
        GetReport.execute(
            GetFormatedReports.execute(excel_path=reports),
            GetFormatedMovements.execute(excel_path=movements)[0],
            self.excel_builder,
            masivo_list,
        )
        GetReport.execute(
            GetFormatedReports.execute(excel_path=reports),
            GetFormatedMovements.execute(excel_path=movements)[1],
            self.excel_builder,
            masivo_list,
        )
        self.pack_to_save: list[Child] = [
            Child(
                Path("Movimientos"),
                self.excel_builder.build(),
                SuffixTypes.XLSX,
            ),
        ]
        self.masivo_list = Masivo(tuple(masivo_list))
        # self.by_pen = masivo.soles_by_bank()
        # self.by_usd = masivo.dolares_by_bank()

    # def save(self, save_dir: Path): ...

    #     masivo_dir = save_dir / "MASIVO EGRESOS"
    #     masivo_dir_pen = masivo_dir / "SOLES"
    #     masivo_dir_usd = masivo_dir / "DOLARES"

    #     SaveReportMasivoByBank.execute(self.by_pen, masivo_dir_pen)
    #     SaveReportMasivoByBank.execute(self.by_usd, masivo_dir_usd)

    #     # archivo de conciliacion
    #     wb = self.excel_builder.build()
    #     file = save_dir / "movimientos.xlsx"
    #     wb.save(file)

    def masivo(self, period_date: date) -> None:
        masivo_dir = Path("MASIVO EGRESOS")
        pen_dir = masivo_dir / "SOLES"
        usd_dir = masivo_dir / "DOLARES"
        by_pen = self.masivo_list.soles_by_bank()
        by_usd = self.masivo_list.dolares_by_bank()
        for name_sheet, report in by_pen.items():
            by_pen[name_sheet] = DuplicateMasivo.execute(list(report))
        for name_sheet, report in by_usd.items():
            by_usd[name_sheet] = DuplicateMasivo.execute(list(report))

        # se obtien los masivos de los bancos
        MasivoByBank.execute(by_pen, pen_dir, self.pack_to_save)
        MasivoByBank.execute(by_usd, usd_dir, self.pack_to_save)
        MasivoByDate.execute(by_pen, pen_dir, self.pack_to_save, period_date)
        MasivoByDate.execute(by_pen, usd_dir, self.pack_to_save, period_date)
        # masivo por fechas de cada banco
        # self.file_type: FileType = FileType.XLSX
        self.children = tuple(self.pack_to_save)
