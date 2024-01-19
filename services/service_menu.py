from models.models_restaurant import Menu, Submenu, Dishes
from sqlalchemy.orm import Session
from dto import dto_menu
from uuid import UUID


class DbService:
    def __init__(self, model):
        self.model = model

    def create_menu(
        self, data: dto_menu.Menu | dto_menu.Submenu | dto_menu.Dishes, db: Session
    ):
        self.table = self.model(title=data.title, description=data.description)
        try:
            db.add(self.table)
            db.commit()
            db.refresh(self.table)
        except Exception as e:
            print(e)
            return False
        return self.table

    def get_value_menu(self, id: UUID, db: Session):
        try:
            self.table = db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            print(e)
            return False
        return self.table

    def get_all_menus(self, db: Session):
        return db.query(self.model).all()

    def update_menu(self, data: dto_menu.Menu, db: Session, id: UUID):
        self.table = db.query(self.model).filter(self.model.id == id).first()
        self.table.title = data.title
        db.add(self.table)
        db.commit()
        db.refresh(self.table)
        return self.table

    def remove_menu(self, db: Session, id: UUID):
        self.table = db.query(self.model).filter(self.model.id == id).delete()
        db.commit()
        return self.table

    def __clear_tables(self, db: Session):
        db.query(self.model).delete()
        db.commit()
