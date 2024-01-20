from models.models_restaurant import Menu, Submenu, Dishes
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Union

from sqlalchemy.exc import IntegrityError


class DbService:
    def __init__(self, model):
        self.model = model

    def create(
        self,
        db: Session,
        data: Union[Menu, Submenu, Dishes],
        id: UUID = None,
        menu_id: UUID = None,
        submenu_id: UUID = None,
    ):
        data_dict = data.dict()
        if "price" in data_dict:
            data_dict["price"] = str(float(data_dict["price"]))
        table = self.model(**data_dict)
        if id is not None:
            table.id = id
        if menu_id is not None:
            table.menu_id = menu_id
        if submenu_id is not None:
            table.submenu_id = submenu_id
        try:
            db.add(table)
            db.commit()
            db.refresh(table)
        except IntegrityError as e:
            print(e)
            return False
        return table

    def get_value(self, db: Session, id: UUID = None):
        if id:
            result = db.query(self.model).filter(self.model.id == id).first()
            if self.model == Menu and result is not None:
                submenus_count = db.query(Submenu).filter(Submenu.menu_id == id).count()
                dishes_count = (
                    db.query(Dishes)
                    .join(Submenu, Dishes.submenu_id == Submenu.id)
                    .filter(Submenu.menu_id == id)
                    .count()
                )
                result.submenus_count = submenus_count
                result.dishes_count = dishes_count
            elif self.model == Submenu and result is not None:
                dishes_count = db.query(Dishes).filter(Dishes.submenu_id == id).count()
                result.dishes_count = dishes_count
            elif self.model == Dishes and result is not None:
                result.price = str(float(result.price))
            return result

    def get_all(self, db: Session, id: UUID = None):
        all_values = db.query(self.model).all()
        return all_values

    def update(
        self,
        db: Session,
        data: Union[Menu, Submenu, Dishes],
        id: UUID = None,
    ):
        table = db.query(self.model).filter(self.model.id == id).first()
        for key, value in data.dict().items():
            setattr(table, key, value)
        db.add(table)
        db.commit()
        db.refresh(table)
        return table

    def remove(self, db, id):
        table = db.query(self.model).filter(self.model.id == id).delete()
        db.commit()
        return table
