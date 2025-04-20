import pytest
from auth import get_password_hash, create_access_token
import main
from database import ParkingSlot, Admin


def test_parking_status_empty(client):
    response = client.get("/parking_status")
    assert response.status_code == 200
    assert response.json() == []


def test_book_and_release_flows(db, client, monkeypatch):
    # Add a slot
    slot = ParkingSlot(slot_id="S1", status=True, user=None)
    db.add(slot)
    db.commit()

    # Stub Google token verification
    monkeypatch.setattr(main, "verify_google_token", lambda token: {"email": "u@x.com"})

    # Book slot
    resp = client.post("/book/S1?token=tok")
    assert resp.status_code == 200
    assert "successfully booked" in resp.json()["message"]

    # Attempt to book non-existent slot
    resp = client.post("/book/NOPE?token=tok")
    assert resp.status_code == 404

    # Attempt to book already booked
    resp = client.post("/book/S1?token=tok")
    assert resp.status_code == 400

    # Release slot
    resp = client.post("/release/S1")
    assert resp.status_code == 200
    assert "successfully released" in resp.json()["message"]

    # Release non-existent
    resp = client.post("/release/X?token=tok")
    assert resp.status_code == 404

    # Release already available
    resp = client.post("/release/S1")
    assert resp.status_code == 400


def test_admin_login_and_slot_management(db, client):
    # No admin yet: login fails
    resp = client.post("/admin/login?username=a&password=b")
    assert resp.status_code == 401

    # Create admin in DB
    hashed = get_password_hash("pw")
    admin = Admin(username="a", hashed_password=hashed)
    db.add(admin)
    db.commit()

    # Successful login
    resp = client.post("/admin/login?username=a&password=pw")
    assert resp.status_code == 200
    token = resp.json().get("access_token")
    assert token

    headers = {"Authorization": f"Bearer {token}"}

    # Add slot
    resp = client.post("/admin/add_slot/A1", headers=headers)
    assert resp.status_code == 200

    # Add existing slot
    resp = client.post("/admin/add_slot/A1", headers=headers)
    assert resp.status_code == 400

    # Delete non-existent
    resp = client.delete("/admin/delete_slot/B1", headers=headers)
    assert resp.status_code == 404

    # Delete existing
    resp = client.delete("/admin/delete_slot/A1", headers=headers)
    assert resp.status_code == 200


def test_user_and_verify_admin_endpoints(client, monkeypatch):
    # Stub Google verify
    monkeypatch.setattr(main, "verify_google_token", lambda token: {"email": "foo@bar.com"})
    resp = client.get("/user?token=tok")
    assert resp.status_code == 200
    assert resp.json()["user"] == "foo@bar.com"

    # Stub current admin dependency
    class DummyAdmin:
        username = "adminX"

    main.app.dependency_overrides[main.get_current_admin] = lambda: DummyAdmin()
    resp = client.get("/admin/verify", headers={"Authorization": "Bearer any"})
    assert resp.status_code == 200
    assert resp.json()["username"] == "adminX"
