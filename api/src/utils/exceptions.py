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


class TokenAuthenticationSchemaError(Exception):
    """Raised when JWT token schema authentication fails."""


class InvalidTokenError(Exception):
    """Raised when JWT token is invalid or expired."""


class TokenAuthenticationCodeError(Exception):
    """Raised when JWT token code authentication fails."""
