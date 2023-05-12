"""
Module to handle JWT token.

This module handles JWT token operations like JWT token creation and token decoding.
"""

import logging
import time

import jwt
from src.utils.exceptions import TokenDecodingError
from src.config.settings import settings


def token_response(token: str) -> dict[str, str]:
    """Prepare JWT token response body.

    :param token: JWT token.
    :type token: str
    :returns: JWT token response body.
    :rtype: dict
    """

    return {"access_token": token}


def create_token() -> dict[str, str]:
    """Create JWT token.

    :returns: JWT token with response body representation.
    :rtype: dict
    """

    payload = {"expires": time.time() + settings.jwt_token_expiration}

    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token_response(token)


def decode_token(token: str) -> dict[str, str]:
    """Decode JWT token.

    :param token: JWT token.
    :type token: str
    :returns: Decoded JWT token.
    :rtype: dict
    """
    try:
        decoded_token = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as err:
        logging.error(f"Caught exception during JWT token decoding: {err}")
        raise TokenDecodingError from err
