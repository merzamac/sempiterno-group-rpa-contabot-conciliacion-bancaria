from contabot_conciliacion_bancaria.process.shared.domain.models import FileToUpload
from contabot_conciliacion_bancaria.processor.strategy import (
    AppBasedProcessor,
)
from contabot_conciliacion_bancaria.path_reader.domain.models import (
    ProcessableDirectory,
)
from pathlib import Path
from contabot_conciliacion_bancaria.process.conciliacion.infrastructure.repositories import (
    ConciliacionContainer,
)
from contabot_conciliacion_bancaria.process.shared.domain.repositories import Container
from aconsys.views.login.window import LoginWindow as AconsysApp
from contabot_conciliacion_bancaria import paths
from contabot_conciliacion_bancaria.utils.manager import CredentialManager
from keyring.credentials import Credential
from loguru import logger
from datetime import date, timedelta
from contabot_conciliacion_bancaria.notification.models import Notification


class ConciliacionProcessor(AppBasedProcessor):
    def get_container(self, element_path: Path) -> Container:
        return ConciliacionContainer(element_path)

    def process(
        self, processable_directory: ProcessableDirectory, save_directory: Path
    ) -> None:
        container = self.get_container(processable_directory.element_path)
        container.conciliar()
        logger.info("La Conciliacin fue realizada...")
        period_date = self.get_date(processable_directory.get_period_date)
        container.masivo(period_date=period_date)
        logger.info("Los Masivos fueron creados..")
        files_to_upload: tuple[FileToUpload, ...] = container.save(save_directory)

        self.process_with_app(
            files_to_upload, date_=period_date, save_directory=save_directory
        )

    def get_date(self, date: date) -> date:
        # date end, previous month

        return date.replace(day=1) - timedelta(days=1)

    def process_with_app(
        self,
        file_to_upload: tuple[FileToUpload, ...],
        date_: date,
        save_directory: Path,
    ) -> None:
        credentials: Credential = CredentialManager.get_credential(
            service_name="Aconsys"
        )

        with AconsysApp(paths.APP_PATH, credentials) as app:
            # app.change_work_period()
            app.change_work_period(date_)
            logger.info(f"Work period {date_}")
            accounting_window = app.accounting_entry_process_from_excel()
            notification: Notification = Notification()
            for file in file_to_upload:

                accounting_window.set_date_and_type_operation(
                    file.date, file.type_transaction
                )
                accounting_window.set_file_path(file.file_path)
                logger.info(
                    f"Date: {file.date}, Type of Operation: {file.type_transaction}, file: {file.file_path}"
                )
                validation_message = accounting_window.get_validation()
                logger.info(f"Validation result '{validation_message}'")
                if "Inconsistencia" in validation_message:
                    result = accounting_window.get_process_result()
                    continue

                notification.add_warning(file.file_path.name)
                notification.add_warning(validation_message)
                notification.add_warning("")

            notification.create_file(save_directory)
