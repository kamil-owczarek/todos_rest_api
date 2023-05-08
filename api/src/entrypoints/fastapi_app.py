from fastapi import FastAPI
from src.domain.model import Item

app = FastAPI()


@app.get("/items", response_model=Item)
def get_items():
    pass


@app.get("/items/{item_id}", response_model=list[Item])
def get_item(item_id: int):
    pass


@app.post("/items")
def post_item(item: Item):
    pass


@app.patch("/items/{item_id}")
def update_item(item_id: int, item: Item):
    pass


@app.delete("/items/{item_id}")
def delete_itme(item_id: int):
    pass
