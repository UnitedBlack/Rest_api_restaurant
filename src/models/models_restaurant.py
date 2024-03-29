from sqlalchemy import Column, String, DECIMAL, ForeignKey
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
    title = Column(String, unique=True)
    description = Column(String)
    price = Column(DECIMAL(precision=10, scale=2))
    submenu_id = Column(
        UUID(as_uuid=True), ForeignKey("submenus.id", ondelete="CASCADE")
    )
    submenu = relationship("Submenu", back_populates="dishes")
