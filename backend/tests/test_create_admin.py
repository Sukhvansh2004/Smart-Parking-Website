import pytest
from create_admin import create_admin
from auth import get_password_hash

def test_create_new_admin(db, capsys):
    # Create a fresh admin
    create_admin("admin1", "password123")
    captured = capsys.readouterr()
    assert "Admin 'admin1' created successfully" in captured.out

    # Now import the model *after* the test DB is in place
    from database import Admin
    admin = db.query(Admin).filter(Admin.username == "admin1").first()
    assert admin is not None
    # Ensure password was hashed
    assert admin.hashed_password != "password123"

def test_create_existing_admin(db, capsys):
    # First creation succeeds
    create_admin("admin2", "pw")
    # Second creation should short-circuit
    create_admin("admin2", "pw")
    captured = capsys.readouterr()
    assert "Admin already exists" in captured.out
