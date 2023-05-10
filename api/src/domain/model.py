from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, index=True, default=False)


class ItemBaseSchema(BaseModel):
    title: str
    description: str
    completed: bool = False


class ItemSchema(ItemBaseSchema):
    id: int

    class Config:
        orm_mode = True
