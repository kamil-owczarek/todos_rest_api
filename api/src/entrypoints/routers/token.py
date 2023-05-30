"""
Module contains FastAPI token routes.
"""


from fastapi import APIRouter
from src.auth.token_handler import create_token

router = APIRouter(prefix="/token", tags=["token"])


@router.get("", description="Generate authentication token.")
def get_token():
    """Generate JWT token.

    :returns: JWT token with response body representation.
    :rtype: dict
    """

    return create_token()
