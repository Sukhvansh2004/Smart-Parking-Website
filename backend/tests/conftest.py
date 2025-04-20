import os
import sys
import pytest
import importlib

# Make sure the backend package is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture(autouse=True)
def env_and_db(tmp_path_factory, monkeypatch):
    # 1) Spin up a fresh SQLite file under a temp dir
    temp_dir = tmp_path_factory.mktemp("db")
    db_file = temp_dir / "test.db"
    sqlite_url = f"sqlite:///{db_file}"

    # 2) Override all secrets/envs for tests
    monkeypatch.setenv("DATABASE_URL", sqlite_url)
    monkeypatch.setenv("SECRET_KEY", "testsecret")
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "testclientid")
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "testclientsecret")

    # 3) Reload every module that reads those at import-time
    import database
    import main
    import secret
    import create_admin
    import auth

    importlib.reload(database)
    importlib.reload(main)
    importlib.reload(secret)
    importlib.reload(create_admin)
    importlib.reload(auth)

    # 4) Create all tables in the test SQLite
    from database import Base, engine
    Base.metadata.create_all(bind=engine)

    yield

    # 5) Tear down
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    from database import SessionLocal
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from main import app
    return TestClient(app)
