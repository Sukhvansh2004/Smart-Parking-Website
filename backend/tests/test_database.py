from database import SessionLocal, ParkingSlot, Admin, init_db


def test_init_db_runs_without_error():
    # Should create tables without raising
    init_db()


def test_parking_slot_crud(db):
    slot = ParkingSlot(slot_id="A1", status=True, user=None)
    db.add(slot)
    db.commit()
    queried = db.query(ParkingSlot).filter(ParkingSlot.slot_id == "A1").first()
    assert queried is not None
    assert queried.status
    assert queried.user is None


def test_admin_model_crud(db):
    admin = Admin(username="admin1", hashed_password="hashp")
    db.add(admin)
    db.commit()
    queried = db.query(Admin).filter(Admin.username == "admin1").first()
    assert queried is not None
    assert queried.hashed_password == "hashp"
