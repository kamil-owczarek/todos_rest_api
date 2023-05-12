"""
Module contains implementation of custom exceptions.
"""


class IdNotFound(Exception):
    """Raised when Item id does not exist."""


class KeyVaultConnectionError(Exception):
    """Raised when Key Vault connection error occurs."""


class SecretError(ValueError):
    """Raised when Key Vault secret does not exist."""


class TokenDecodingError(Exception):
    """Raised when JWT token decoding fails."""
