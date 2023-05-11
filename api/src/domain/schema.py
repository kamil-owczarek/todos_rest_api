from pydantic import BaseModel


class ItemBaseSchema(BaseModel):
    title: str
    description: str
    completed: bool = False


class ItemSchema(ItemBaseSchema):
    id: int

    class Config:
        orm_mode = True
