import logging

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from src.utils.exceptions import KeyVaultConnectionError, SecretError


class AzureVault:
    def __init__(self, key_vault_url: str):
        try:
            self.secret_client = SecretClient(
                vault_url=key_vault_url, credential=DefaultAzureCredential()
            )
        except Exception as err:
            logging.error(
                f"Caught exception during connection to Azure Key Vault: {err}"
            )
            raise KeyVaultConnectionError

    def get_secret(self, secret_name: str) -> str:
        try:
            return self.secret_client.get_secret(secret_name).value
        except Exception as err:
            logging.error(
                f"Caught exception during getting secret value from Azure Key Vault: {err}"
            )
            raise SecretError
