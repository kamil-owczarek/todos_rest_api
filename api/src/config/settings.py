"""
Module to create base API configuration.

This module creates Settings object with API configuration
"""

import json
import os

from pydantic import BaseSettings
from src.azure.key_vault import AzureVault


class Settings(BaseSettings):
    """
    Settings object creates API configuration based on environment variables.

    :param jwt_secret: JWT token encoding secret.
    :type jwt_secret: str
    :param jwt_algorithm: JWT token encoding and decoding algorithm. Default: HS256.
    :type jwt_algorithm: str
    :param jwt_token_expiration: JWT token expiration time in seconds. Default: 600.
    :type jwt_token_expiration: int
    :param db_user: Database user name.
    :type db_user: str
    :param db_password: Database user password.
    :type db_password: str
    :param db_host: Database host.
    :type db_host: str
    :param db_port: Database port.
    :type db_port: int
    :param db_name: Database name.
    :type db_name: str
    """

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_token_expiration: int = 600
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    db_table_name: str = "items"


def prepare_settings() -> Settings:
    """
    Prepare Settings object based on credential type.
    Credentials can be read from Azure Key Vault or environmental varables

    :returns: Base API configuration.
    :rtype: Settings
    """

    credential_type = os.environ.get("credential_type")
    if credential_type == "cloud":
        key_vault = AzureVault(os.environ.get("key_vault_url"))
        secrets = json.loads(os.environ.get("azure_secrets"))
        return Settings(
            **{
                secret.replace("-", "_"): key_vault.get_secret(secret)
                for secret in secrets
            }
        )
    return Settings()


settings = prepare_settings()
