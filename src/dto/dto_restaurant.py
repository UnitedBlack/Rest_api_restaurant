from pydantic import BaseModel
from typing import Union, ClassVar


class Menu(BaseModel):
    title: str
    description: str

    Config: ClassVar = {"from_attributes": True}


class Submenu(BaseModel):
    title: str
    description: str

    Configs: ClassVar = {"from_attributes": True}


class Dishes(BaseModel):
    title: str
    description: str
    price: Union[float, str]

    Config: ClassVar = {"from_attributes": True}
