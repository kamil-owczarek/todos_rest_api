from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.utils.exceptions import (
    IdNotFound,
    InvalidTokenError,
    TokenAuthenticationCodeError,
    TokenAuthenticationSchemaError,
    TokenDecodingError,
)


def exception_handlers(app: FastAPI):
    app.add_exception_handler(Exception, internal_server_error_handler)
    app.add_exception_handler(IdNotFound, id_not_found_error_handler)
    app.add_exception_handler(TokenDecodingError, decoding_token_error_handler)
    app.add_exception_handler(
        TokenAuthenticationSchemaError, token_authentication_schema_error_handler
    )
    app.add_exception_handler(InvalidTokenError, invalid_token_error_handler)
    app.add_exception_handler(
        TokenAuthenticationCodeError, token_authentication_code_error_handler
    )


def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content="Internal Server Error",
    )


def id_not_found_error_handler(request: Request, exc: IdNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content="ID not found!",
    )


def decoding_token_error_handler(request: Request, exc: TokenDecodingError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content="Invalid token",
    )


def token_authentication_schema_error_handler(
    request: Request, exc: TokenAuthenticationSchemaError
):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content="Invalid authentication scheme",
    )


def invalid_token_error_handler(request: Request, exc: InvalidTokenError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content="Invalid token or expired token"
    )


def token_authentication_code_error_handler(
    request: Request, exc: TokenAuthenticationCodeError
):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content="Invalid authorization code"
    )
