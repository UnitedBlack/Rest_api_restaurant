import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import (
    DB_USER_TEST,
    DB_PASS_TEST,
    DB_NAME_TEST,
    DB_HOST_TEST,
    DB_PORT_TEST,
)
from database import get_db, Base
from main import app

DATABASE_URL_TEST = f"postgresql://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_engine(DATABASE_URL_TEST)
SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = SessionLocalTest()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope="session")
def prepare_database():
    with engine_test.begin() as conn:
        Base.metadata.create_all(bind=engine_test)
    yield
    with engine_test.begin() as conn:
        Base.metadata.drop_all(bind=engine_test)


client = TestClient(app)
# Base.metadata.reflect(bind=engine_test)
# Base.metadata.drop_all(bind=engine_test)
