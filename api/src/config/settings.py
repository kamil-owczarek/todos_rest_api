import json
import os

from pydantic import BaseSettings
from src.azure.key_vault import AzureVault


class Settings(BaseSettings):
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_token_expiration: int = 600
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str


def prepare_settings() -> Settings:
    env = os.environ.get("credential_type")
    if env == "local":
        return Settings()
    if env == "cloud":
        key_vault = AzureVault(os.environ.get("key_vault_url"))
        secrets = json.loads(os.environ.get("azure_secrets"))
        return Settings(
            **{
                secret.replace("-", "_"): key_vault.get_secret(secret)
                for secret in secrets
            }
        )


settings = prepare_settings()
