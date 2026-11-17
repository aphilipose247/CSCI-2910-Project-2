import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Operator
from app.scripts.populate_db import operators_data

# This file contains the fixtures needed for the tests
# Fixtures are used to prepare something, while a test checks something
# A fixture helps set up what a test needs

# A throwaway database that lives in memory (RAM) and disappears when the tests finish.
# Creating another database to ensure we don't affect the real db (in this case, operators.db)

test_engine = create_engine(
    "sqlite:///:memory:", #this helps create the db within memory, this is important
    connect_args={"check_same_thread": False},
    poolclass=StaticPool, # Makes every connection share that one in-memory database, otherwise each connection would get its own copy of the data
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def get_test_db(): #another db is called test_db
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session") #	Create one client (fake browser) and share it across all the tests, instead of building a new one for every test
def client(): # this is needed to help send HTTPS requests (like post, get, put, etc.) to your app without having to start a server, which allows the test to be down quickly 
    """A fake browser that sends requests straight to the app, using the test database."""
    app.dependency_overrides[get_db] = get_test_db #Remember Depends(get_db) from Lab 5? This swaps it out, so every endpoint gets the test database instead of the real one
    with TestClient(app) as c:
        yield c #Everything before yield is setup, and everything after is cleanup
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True) #Run reset_db before every test automatically, even though no test asks for it by name. This helps reset everything before running the tests
def reset_db():
    """Runs before EVERY test: start each one with empty tables."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield


@pytest.fixture
def seeded_db(): #Tests that ask for this fixture get the 10 real operators. Tests that don't start with an empty table.
    """Fill the test database with the same 10 operators the real db starts with."""
    with TestingSessionLocal() as db:
        db.add_all(Operator(**operator) for operator in operators_data)
        db.commit()
    return operators_data


@pytest.fixture
def sample_operator(): # returns a dict you can send as a POST body for an operator that is NOT in the seed data. This makes it where you don't have to type these 7 fields for every test you do
    return {
    "operator_name": "Coffey",
    "real_name": "Unknown",
    "faction": "JSOF",
    "nationality": "United States",
    "language": "English",
    "is_available": True,
    "image_of_operator" : "https://api.mw4.gg/api/v2/media/v2/operator/op-coffey/bioImage.webp?v=1792430497236",
}

@pytest.fixture
def updated_operator(): #returns a dict that you can send as a PUT body. This helps put the updated operator to the id of the created operator to show that an update has happened
    return {
    "operator_name": "Ju Kwon",
    "real_name": "Ju Kwon",
    "faction": "South Korean Quick Reaction Force",
    "nationality": "South Korea",
    "language": "Korean",
    "is_available": False,
    "image_of_operator" : "https://api.mw4.gg/api/v2/media/v2/operator/op-ju-kwon/bioImage.webp?v=1792526639963"
}

@pytest.fixture #This saves you from writing "create an operator first" at the top of every update and delete test.
def created_operator(client, sample_operator):
    response = client.post("/operators/", json = sample_operator)
    assert response.status_code == 201
    return response.json()