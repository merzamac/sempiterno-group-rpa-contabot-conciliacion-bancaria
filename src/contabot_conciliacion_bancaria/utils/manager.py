from getpass import getpass
from keyring import get_credential, set_password
from keyring.credentials import Credential


class CredentialManager:
    @classmethod
    def get_credential(cls, service_name: str ) -> Credential:
        while not (credentials := get_credential(service_name, None)):
            creds: dict[str, str] = cls.get_data()
            set_password(
                service_name=service_name, username=creds["username"], password=creds["password"]
            )
        return credentials

    @classmethod
    def get_data(cls):
        username = input("Enter your Aconsys username: ").strip()
        password = getpass("Enter your Aconsys password: ")
        return {"username": username, "password": password}

    # @classmethod
    # def get(cls, service_name: str = "Aconsys") -> Dict[str, str]:
    #     return loads(cls.get_credential(service_name).password)