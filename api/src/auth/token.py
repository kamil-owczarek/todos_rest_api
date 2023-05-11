from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.token_handler import decode_token


class JWTToken(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTToken, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTToken, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_token(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_token(self, token: str) -> bool:
        is_token_valid = False
        try:
            payload = decode_token(token)
        except:
            payload = None

        if payload:
            is_token_valid = True
        return is_token_valid
