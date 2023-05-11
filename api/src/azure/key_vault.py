from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class AzureVault:
    def __init__(self, key_vault_url: str):
        self.secret_client = SecretClient(
            vault_url=key_vault_url, credential=DefaultAzureCredential()
        )

    def get_secret(self, secret_name: str) -> str:
        try:
            return self.secret_client.get_secret(secret_name).value
        except Exception as err:
            raise err
