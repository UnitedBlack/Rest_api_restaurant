from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_USER, DB_PASS, DB_NAME, DB_HOST, DB_PORT

SQLALCHEMY_URL = "postgresql://restaurant_admin:restaurant_password@localhost:5432/menus"

engine = create_engine(SQLALCHEMY_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
