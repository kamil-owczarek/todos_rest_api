import logging
import os

from fastapi import Depends, FastAPI, HTTPException, Query, Response
from src.auth.token import JWTToken
from src.auth.token_handler import create_token
from src.domain.model import ItemBaseSchema, ItemSchema
from src.service import services
from src.service.unit_of_work import PostgresUnitOfWork
from src.utils.exceptions import IdNotFound

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


connection = {
    "username": os.environ.get("db_user", "postgres"),
    "password": os.environ.get("db_password", "test1234"),
    "host": os.environ.get("db_host", "localhost"),
    "port": int(os.environ.get("db_port", "5432")),
    "database_name": os.environ.get("db_name", "postgres"),
}


@app.get(
    "/items",
    response_model=list[ItemSchema],
    dependencies=[Depends(JWTToken())],
    description="Retrieve todo items based on the provided filters.",
)
def get_items(
    limit: int = Query(20, ge=0),
    offset: int = Query(0, ge=0),
    filter_field: str | None = Query(None),
    filter_value: str | bool | None = Query(None),
):
    try:
        results = services.get_items(
            limit,
            offset,
            filter_field,
            filter_value,
            uow=PostgresUnitOfWork(connection),
        )
        if not results:
            return Response(status_code=204)
        return results
    except Exception as err:
        logging.error(f"Caught error during getting Items: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get(
    "/items/{item_id}",
    response_model=ItemSchema,
    dependencies=[Depends(JWTToken())],
    description="Retrieve todo item based on the provided ID.",
)
def get_item(item_id: int):
    try:
        return services.get_item(item_id, uow=PostgresUnitOfWork(connection))
    except IdNotFound:
        raise HTTPException(
            status_code=404, detail=f"Item with ID: {item_id} not found!"
        )
    except Exception as err:
        logging.error(f"Caught error during getting Item: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post(
    "/items",
    dependencies=[Depends(JWTToken())],
    description="Upload todo item with provided title, description and completed flag.",
)
def post_item(item: ItemBaseSchema):
    try:
        services.insert_item(item, uow=PostgresUnitOfWork(connection))
        return Response(status_code=201)
    except Exception as err:
        logging.error(f"Caught error during inserting Item: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.patch(
    "/items/{item_id}",
    dependencies=[Depends(JWTToken())],
    description="Update todo item based on ID.",
)
def update_item(item_id: int, item: ItemBaseSchema):
    try:
        services.update_item(item_id, item, uow=PostgresUnitOfWork(connection))
        return Response(status_code=204)
    except IdNotFound:
        raise HTTPException(
            status_code=404, detail=f"Item with ID: {item_id} not found!"
        )
    except Exception as err:
        logging.error(f"Caught error during updating Item: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete(
    "/items/{item_id}",
    dependencies=[Depends(JWTToken())],
    description="Delete todo item based on provided ID.",
)
def delete_item(item_id: int):
    try:
        services.delete_item(item_id, uow=PostgresUnitOfWork(connection))
        return Response(status_code=204)
    except IdNotFound:
        raise HTTPException(
            status_code=404, detail=f"Item with ID: {item_id} not found!"
        )
    except Exception as err:
        logging.error(f"Caught error during Item deletion: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/token", description="Generate authentication token.")
def get_token():
    try:
        return create_token()
    except Exception as err:
        logging.error(f"Caught error during Item deletion: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
