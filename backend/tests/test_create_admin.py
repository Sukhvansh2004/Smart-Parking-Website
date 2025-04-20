import pytest
from create_admin import create_admin
from auth import get_password_hash
from database import SessionLocal, Admin


def test_create_new_admin(db, capsys):
    create_admin("admin1", "password123")
    captured = capsys.readouterr()
    assert "Admin 'admin1' created successfully" in captured.out

    # Verify in DB
    session = SessionLocal()
    admin = session.query(Admin).filter(Admin.username == "admin1").first()
    assert admin is not None
    # The password should be hashed (not equal to plain)
    assert admin.hashed_password != "password123"
    session.close()


def test_create_existing_admin(db, capsys):
    # First creation
    create_admin("admin2", "pw")
    # Attempt again
    create_admin("admin2", "pw")
    captured = capsys.readouterr()
    assert "Admin already exists" in captured.out
