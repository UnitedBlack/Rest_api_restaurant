from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Menu(Base):
    __tablename__ = "menus"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )
    title = Column(String)
    description = Column(String)
    submenus = relationship("Submenu", back_populates="menu")


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )
    name = Column(String, unique=True)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id"))
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu")


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )
    name = Column(String, unique=True)
    price = Column(Integer, primary_key=True)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenus.id"))
    submenu = relationship("Submenu", back_populates="dishes")
