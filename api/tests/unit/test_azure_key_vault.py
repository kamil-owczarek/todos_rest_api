import pytest
from src.azure.key_vault import AzureVault
from src.utils.exceptions import KeyVaultConnectionError, SecretError


def test_get_secret_value(fake_key_vault_client):
    key_vault = AzureVault("https://test_url")
    result = key_vault.get_secret("fake_secret_1")
    assert result == "fake_value_1"


def test_get_secret_value_raise_connection_error(fake_key_vault_client):
    with pytest.raises(KeyVaultConnectionError):
        key_vault = AzureVault("test_url")
        key_vault.get_secret("fake_secret_3")


def test_get_secret_value_raise_secret_error(fake_key_vault_client):
    with pytest.raises(SecretError):
        key_vault = AzureVault("https://test_url")
        key_vault.get_secret("fake_secret_3")
