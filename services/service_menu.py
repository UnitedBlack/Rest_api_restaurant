from models.models_restaurant import Menu, Submenu, Dishes
from sqlalchemy.orm import Session
from dto import dto_restaurant
from uuid import UUID


# изменить названия функциям на menu
class DbService:
    def create_menu(self, data: dto_restaurant.Menu, db: Session):
        self.table = Menu(title=data.title, description=data.description)
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
            self.table = db.query(Menu).filter(Menu.id == id).first()
        except Exception as e:
            print(e)
            return False
        return self.table

    def get_all_menus(self, db: Session):
        return db.query(Menu).all()

    def update_menu(self, data: dto_restaurant.Menu, db: Session, id: UUID):
        self.table = db.query(Menu).filter(Menu.id == id).first()
        self.table.title = data.title
        db.add(self.table)
        db.commit()
        db.refresh(self.table)
        return self.table

    def remove_menu(self, db: Session, id: UUID):
        self.table = db.query(Menu).filter(Menu.id == id).delete()
        db.commit()
        return self.table

    #######################################################################
    def create_submenu(self, data: dto_restaurant.Submenu, id: UUID, db: Session):
        self.table = Submenu(
            title=data.title,
            description=data.description,
            menu_id=id,
        )
        try:
            db.add(self.table)
            db.commit()
            db.refresh(self.table)
        except Exception as e:
            print(e)
            return False
        return self.table

    def get_value_submenu(self, id: UUID, db: Session):
        try:
            self.table = db.query(Submenu).filter(Submenu.id == id).first()
        except Exception as e:
            print(e)
            return False
        return self.table

    def get_all_submenus(self, submenu_id: UUID, db: Session):
        return db.query(Submenu).filter(Submenu.id == submenu_id).all()

    def update_submenu(self, data: dto_restaurant.Submenu, db: Session, id: UUID):
        self.table = db.query(Submenu).filter(Submenu.id == id).first()
        self.table.title = data.title
        db.add(self.table)
        db.commit()
        db.refresh(self.table)
        return self.table

    def remove_submenu(self, db: Session, id: UUID):
        self.table = db.query(Submenu).filter(Submenu.menu_id == id).delete()
        db.commit()
        return self.table
