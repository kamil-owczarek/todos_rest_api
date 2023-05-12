class IdNotFound(Exception):
    """Raised when Item id does not exist."""

    pass


class KeyVaultConnectionError(Exception):
    """Key Vault connection error"""

    pass


class SecretError(ValueError):
    """Secret not found !"""

    pass
