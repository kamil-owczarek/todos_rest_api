"""
Module to create connection with Azure Key Vault.

This module creates connection with Azure Key Vault and retrieve secrets.
"""

import logging

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from src.utils.exceptions import KeyVaultConnectionError, SecretError


class AzureVault:
    """
    AzureVault object creates connectivity to Azure Key Vault to retrieve secrets.

    :param key_vault_url: URL to Azure Key Vault service.
    :type key_vault_url: str
    """

    def __init__(self, key_vault_url: str):
        try:
            self.secret_client = SecretClient(
                vault_url=key_vault_url, credential=DefaultAzureCredential()
            )
        except Exception as err:
            logging.error(
                f"Caught exception during connection to Azure Key Vault: {err}"
            )
            raise KeyVaultConnectionError from err

    def get_secret(self, secret_name: str) -> str:
        """Retrieve secret value from Azure Key Vault based on secret name.

        :param secret_name: Azure Key Vault secret name.
        :type secret_name: str
        :returns: Azure Key Vault secret value.
        :rtype: str
        """
        try:
            return self.secret_client.get_secret(secret_name).value
        except Exception as err:
            logging.error(
                f"Caught exception during getting secret value from Azure Key Vault: {err}"
            )
            raise SecretError from err
