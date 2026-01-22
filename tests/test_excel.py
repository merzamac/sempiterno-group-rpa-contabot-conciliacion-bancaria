from aconsys.views.login.window import LoginWindow as AconsysApp
from contabot_conciliacion_bancaria import paths
from contabot_conciliacion_bancaria.utils.manager import CredentialManager
from keyring.credentials import Credential
from time import sleep
from datetime import date


def test_process_with_app() -> None:
    credentials: Credential = CredentialManager.get_credential(service_name="Aconsys")

    with AconsysApp(paths.APP_PATH, credentials) as app:
        # app.change_work_period()
        # sleep(15)
        app.change_work_period(date.today())
        accounting_window = app.accounting_entry_process_from_excel()
