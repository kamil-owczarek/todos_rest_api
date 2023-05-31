"""
Module to create and verify JWT token.

This module creates JWT token and verify token.
"""

import logging

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.auth.token_handler import decode_token
from src.utils.exceptions import (
    InvalidTokenError,
    TokenAuthenticationCodeError,
    TokenAuthenticationSchemaError,
    TokenDecodingError,
)


class JWTToken(HTTPBearer):
    """
    JWTToken object authorize HTTP request with JWT token.
    """

    def __init__(self, auto_error: bool = True):
        super(JWTToken, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTToken, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise TokenAuthenticationSchemaError
            if not self.verify_token(credentials.credentials):
                raise InvalidTokenError
        else:
            raise TokenAuthenticationCodeError

    def verify_token(self, token: str) -> bool:
        """Verify JWT token.

        :param token: JWT token.
        :type token: str
        :returns: Information that JWT token is valid.
        :rtype: bool
        """

        is_token_valid = False
        try:
            payload = decode_token(token)
        except TokenDecodingError:
            payload = None
        except Exception as err:
            logging.info("Caught exception during token veryfication.")
            raise err

        if payload:
            is_token_valid = True
        return is_token_valid
