import logging
import os
import time

import jwt

JWT_SECRET = os.environ.get("jwt_secret", "test")
JWT_ALGORITHM = os.environ.get("jwt_algorithm", "HS256")
JWT_TOKEN_EXPIRATION = int(os.environ.get("jwt_token_expiration", "600"))


def token_response(token: str) -> dict[str, str]:
    return {"access_token": token}


def create_token() -> dict[str, str]:
    payload = {"expires": time.time() + JWT_TOKEN_EXPIRATION}

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decode_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as err:
        logging.error("Caught exception during JWT token decoding.")
        raise err
