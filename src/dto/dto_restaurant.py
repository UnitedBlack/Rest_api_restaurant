from pydantic import BaseModel
from typing import Union

class Menu(BaseModel):
    title: str
    description: str


class Submenu(BaseModel):
    title: str
    description: str


class Dishes(BaseModel):
    title: str
    description: str
    price: Union[float, str]
