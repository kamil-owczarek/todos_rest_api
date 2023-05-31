"""
Module to create base API configuration.

This module creates Settings object with API configuration
"""

import os

from pydantic import BaseSettings
from src.azure.key_vault import AzureVault


class LocalSettings(BaseSettings):
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


class AzureSettings(LocalSettings):
    class Config:
        def retrieve_azure_secrets(settings: BaseSettings):
            key_vault = AzureVault(os.environ.get("key_vault_url"))
            return {
                field: key_vault.get_secret(field.replace("_", "-"))
                for field in AzureSettings.__fields__
            }

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return (
                init_settings,
                env_settings,
                file_secret_settings,
                cls.retrieve_azure_secrets,
            )


def prepare_settings() -> BaseSettings:
    """
    Prepare Settings object based on credential type.
    Credentials can be read from Azure Key Vault or environmental varables

    :returns: Base API configuration.
    :rtype: Settings
    """

    credential_type = os.environ.get("credential_type")
    if credential_type == "azure":
        return AzureSettings()
    return LocalSettings()


settings = prepare_settings()
