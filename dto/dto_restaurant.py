from pydantic import BaseModel
from uuid import UUID


class Menu(BaseModel):
    title: str
    description: str


class Submenu(BaseModel):
    title: str
    description: str


class Dishes(BaseModel):
    name: str
    price: int
