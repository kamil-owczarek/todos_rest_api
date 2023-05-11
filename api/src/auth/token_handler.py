import logging
import os
import time

import jwt

from src.config.settings import settings


def token_response(token: str) -> dict[str, str]:
    return {"access_token": token}


def create_token() -> dict[str, str]:
    payload = {"expires": time.time() + settings.jwt_token_expiration}

    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token_response(token)


def decode_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as err:
        logging.error("Caught exception during JWT token decoding.")
        raise err
