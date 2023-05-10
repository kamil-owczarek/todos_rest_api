from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    id: Optional[int]
    title: str
    description: str
    completed: bool = False
