from pydantic import BaseModel


class Menu(BaseModel):
    title: str
    description: str


class Submenu(BaseModel):
    title: str
    description: str


class Dishes(BaseModel):
    title: str
    description: str
    price: float
