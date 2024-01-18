from models.model_menu import Menu, Submenu, Dish
from sqlalchemy.orm import Session
from dto import dto_menu


def create_menu(data: dto_menu.Menu, db: Session):
    menu = Menu(title=data.title, description=data.description)
    try:
        db.add(menu)
        db.commit()
        db.refresh(menu)
    except Exception as e:
        print(e)
        return False
    return menu


def get_menu(id: int, db: Session):
    try:
        menu = db.query(Menu).filter(Menu.id == id).first()
    except Exception as e:
        print(e)
        return False
    return menu


def get_all_menus(db: Session):
    return db.query(Menu).all()


def update_menu(data: dto_menu.Menu, db: Session, id: int):
    menu = db.query(Menu).filter(Menu.id == id).first()
    menu.title = data.title
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


def remove_menu(db: Session, id: int):
    menu = db.query(Menu).filter(Menu.id == id).delete()
    db.commit()
    return menu
