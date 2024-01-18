from pydantic import BaseModel, UUID4


class Menu(BaseModel):
    title: str
    description: str



class Submenu(BaseModel):
    name: str


class Dishes(BaseModel):
    name: str
    price: int
