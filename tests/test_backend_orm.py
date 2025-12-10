# tests/test_backend_orm.py
# Mock
# Fixture
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from API.main import app
from API.modules.db_tools import *
import pandas as pd

# Fixture

## create engine
@pytest.fixture(scope="module")
def engine_test():
    return create_engine("sqlite:///:memory:")

## create DB
@pytest.fixture(scope="module")
def setup_db(engine_test):
    Base.metadata.create_all(engine_test)
    yield
    Base.metadata.drop_all(engine_test)

## Insert into DB
@pytest.fixture(scope="module")
def setup_db(engine_test):
    Base.metadata.create_all(engine_test)
    yield
    Base.metadata.drop_all(engine_test)

## create DB Session
@pytest.fixture(scope="function")
def db_session(engine_test, setup_db):
    connection = engine_test.connect()
    transaction = connection.begin()

    SessionTest = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)
    session = SessionTest(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

## Insert test data for read tests
@pytest.fixture(scope="function")
def insert_test_data(db_session):
    data = [
        {'text': 'This is a test'},
        {'text': 'This is a test2'},
    ]
    for row in data:
        quote = Quote(**row)
        db_session.add(quote)
    db_session.commit()

# Mock

## override session local
@pytest.fixture(autouse=True)
def override_get_db_session(monkeypatch, db_session):
    '''Mock get db session'''
    def mock_get_db_session():
        return db_session
    monkeypatch.setattr('API.modules.db_tools.get_db_session', mock_get_db_session)

# Test

def test_add_row_db():
    quote = 'This is a test'
    dict = {'id':1, 'text':quote}
    citation = add_row_db(quote)
    assert  citation == dict


def test_read_db():
    # Wanted
    quotes = [{'id':1 , 'text':'This is a test'}, {'id':2 , 'text':'This is a test2'}]
    # Creation of a wor
    quote = 'This is a test'
    dict = {'id':1, 'text':quote}
    citation = add_row_db(quote)

    quote = 'This is a test2'
    dict = {'id':2, 'text':quote}
    citation = add_row_db(quote)
    # Read DB
    quotes_db = read_db()
    # Verify
    assert  quotes_db == quotes

def test_read_db_2(insert_test_data): 
    quotes = [{'id':1 , 'text':'This is a test'}, {'id':2 , 'text':'This is a test2'}]
    quotes_db = read_db()
    assert  quotes_db == quotes

def test_read_id_db(insert_test_data): 
    quotes = [{'id':1}, {'id':2}]
    quotes_db = read_id_db()
    assert  quotes_db == quotes