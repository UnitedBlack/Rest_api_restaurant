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
    title = Column(String)
    description = Column(String)
    dishes_count = Column(Integer, index=True, default=0)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id", ondelete="CASCADE"))
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dishes", back_populates="submenu")


class Dishes(Base):
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