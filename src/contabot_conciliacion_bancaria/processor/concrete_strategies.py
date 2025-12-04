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
from time import sleep


class ConciliacionProcessor(AppBasedProcessor):
    def get_container(self, element_path: Path) -> Container:
        return ConciliacionContainer(element_path)

    def process(
        self, processable_directory: ProcessableDirectory, save_directory: Path
    ) -> None:
        container = self.get_container(processable_directory.element_path)
        container.conciliar()
        container.masivo(period_date=processable_directory.get_period_date)
        files_to_upload: tuple[FileToUpload, ...] = container.save(save_directory)
        self.process_with_app(files_to_upload)

    def process_with_app(self, file_to_upload: tuple[FileToUpload, ...]) -> None:
        credentials: Credential = CredentialManager.get_credential(
            service_name="Aconsys"
        )
        with AconsysApp(paths.APP_PATH, credentials) as app:
            # app.change_work_period()
            app.change_work_period()
            accounting_window = app.accounting_entry_process_from_excel()
            for file in file_to_upload:

                accounting_window.set_date_and_type_operation(
                    file.date, file.type_transaction
                )
                accounting_window.set_file_path(file.file_path)
                sleep(10)
                # accounting_window.get_validation()
