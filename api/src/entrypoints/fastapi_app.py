"""
Module contains FastAPI configuration.
"""


from fastapi import FastAPI
from src.entrypoints.routers import items, token

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

app.include_router(token.router)
app.include_router(items.router)
