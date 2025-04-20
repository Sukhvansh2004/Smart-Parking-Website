import os
import sys
import pytest
import importlib

# Ensure project root is in path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(autouse=True)
def env_and_db(tmp_path_factory, monkeypatch):
    # Configure an SQLite database file under a temp directory
    temp_dir = tmp_path_factory.mktemp("db")
    db_file = temp_dir / "test.db"
    db_url = f"sqlite:///{db_file}"
    monkeypatch.setenv("DATABASE_URL", db_url)
    monkeypatch.setenv("SECRET_KEY", "testsecret")
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "testclientid")

    # Reload modules that read env vars
    import database
    import main
    importlib.reload(database)
    importlib.reload(main)

    # Initialize the database schema
    from database import Base, engine
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown: drop all tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    # Provide a fresh DB session for each test
    from database import SessionLocal
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client():
    # TestClient for FastAPI app
    from fastapi.testclient import TestClient
    from main import app
    return TestClient(app)
