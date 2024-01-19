from pydantic import BaseModel


class Menu(BaseModel):
    title: str
    description: str


class Submenu(BaseModel):
    title: str
    description: str
    dishes_count: int


class Dishes(BaseModel):
    name: str
    price: int
