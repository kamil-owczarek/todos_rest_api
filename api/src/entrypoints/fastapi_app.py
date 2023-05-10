import os
from fastapi import FastAPI, HTTPException, Response
from src.domain.model import Item
from src.service import services
from src.service.unit_of_work import PostgresUnitOfWork
from src.utils.exceptions import IdNotFound

app = FastAPI()

connection = {
    "username": os.environ.get("db_user"),
    "password": os.environ.get("db_password"),
    "host": os.environ.get("db_host"),
    "port": int(os.environ.get("db_port", "5432")),
    "database_name": os.environ.get("db_name"),
}


@app.get("/items", response_model=list[Item])
def get_items():
    try:
        results = services.get_items(uow=PostgresUnitOfWork(connection))
        if not results:
            return Response(status_code=204)
        return results
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    try:
        return services.get_item(item_id, uow=PostgresUnitOfWork(connection))
    except IdNotFound:
        raise HTTPException(
            status_code=404, detail=f"Item with ID: {item_id} not found!"
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/items")
def post_item(item: Item):
    try:
        services.insert_item(item, uow=PostgresUnitOfWork(connection))
        return Response(status_code=201)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.patch("/items/{item_id}")
def update_item(item_id: int, item: Item):
    try:
        services.update_item(item_id, item, uow=PostgresUnitOfWork(connection))
        return Response(status_code=204)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    try:
        services.delete_item(item_id, uow=PostgresUnitOfWork(connection))
        return Response(status_code=204)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
