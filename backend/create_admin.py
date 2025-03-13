from sqlalchemy.orm import Session
from database import SessionLocal, Admin, init_db
from auth import get_password_hash


def create_admin(username: str, password: str):
    db: Session = SessionLocal()
    init_db()  # ensure tables exist
    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin:
        print("Admin already exists")
        return
    hashed_password = get_password_hash(password)
    new_admin = Admin(username=username, hashed_password=hashed_password)
    db.add(new_admin)
    db.commit()
    print(f"Admin '{username}' created successfully")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python create_admin.py <username> <password>")
    else:
        username = sys.argv[1]
        password = sys.argv[2]
        create_admin(username, password)
