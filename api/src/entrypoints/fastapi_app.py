"""
Module contains FastAPI configuration.
"""


from fastapi import Depends, FastAPI
from src.auth.token import JWTToken
from src.entrypoints.routers import items, token
from src.utils.exception_handlers import exception_handlers

app = FastAPI(
    title="Todo Items REST API",
    description="Todo Items REST API to retrieve todo items.",
    version="0.0.1",
    contact={
        "name": "Kamil Owczarek",
        "email": "kamil.owczarek03@gmail.com",
    },
    docs_url="/docs",
    openapi_url="/openapi.json",
)


exception_handlers(app)

app.include_router(token.router)
app.include_router(items.router, dependencies=[Depends(JWTToken())])
