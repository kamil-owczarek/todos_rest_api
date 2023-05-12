"""
Module contains FastAPI token routes.
"""

import logging

from fastapi import APIRouter, HTTPException
from src.auth.token_handler import create_token

router = APIRouter(prefix="/token", tags=["token"])


@router.get("", description="Generate authentication token.")
def get_token():
    """Generate JWT token.

    :returns: JWT token with response body representation.
    :rtype: dict
    """

    try:
        return create_token()
    except Exception as err:
        logging.error(f"Caught error during Item deletion: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
