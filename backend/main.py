from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional

from database import SessionLocal, ParkingSlot, Admin, init_db
from auth import create_access_token, verify_password, decode_access_token

app = FastAPI()

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper to extract token from Authorization header
def get_token(authorization: Optional[str] = Header(None)):
    if authorization:
        parts = authorization.split(" ")
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1]
    raise HTTPException(status_code=401, detail="Invalid or missing token")

# Validate current admin using the token
def get_current_admin(token: str = Depends(get_token), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found")
    return admin

# -----------------------
# Public User Routes
# -----------------------

@app.get("/parking_status")
def get_parking_status(db: Session = Depends(get_db)):
    slots = db.query(ParkingSlot).all()
    return [{"slot_id": slot.slot_id, "status": "Available" if slot.status else "Occupied"} for slot in slots]

@app.post("/book/{slot_id}")
def book_parking_slot(slot_id: str, db: Session = Depends(get_db)):
    slot = db.query(ParkingSlot).filter(ParkingSlot.slot_id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot does not exist")
    if not slot.status:
        raise HTTPException(status_code=400, detail="Slot already booked")
    slot.status = False
    db.commit()
    return {"message": f"Slot {slot_id} successfully booked"}

@app.post("/release/{slot_id}")
def release_parking_slot(slot_id: str, db: Session = Depends(get_db)):
    slot = db.query(ParkingSlot).filter(ParkingSlot.slot_id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot does not exist")
    if slot.status:
        raise HTTPException(status_code=400, detail="Slot already available")
    slot.status = True
    db.commit()
    return {"message": f"Slot {slot_id} successfully released"}

# -----------------------
# Admin Routes
# -----------------------

@app.post("/admin/login")
def admin_login(username: str, password: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin or not verify_password(password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": admin.username})
    return {"access_token": token}

@app.post("/admin/add_slot/{slot_id}")
def add_slot(slot_id: str, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    if db.query(ParkingSlot).filter(ParkingSlot.slot_id == slot_id).first():
        raise HTTPException(status_code=400, detail="Slot already exists")
    new_slot = ParkingSlot(slot_id=slot_id, status=True)
    db.add(new_slot)
    db.commit()
    return {"message": f"Slot {slot_id} added successfully"}

@app.delete("/admin/delete_slot/{slot_id}")
def delete_slot(slot_id: str, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    slot = db.query(ParkingSlot).filter(ParkingSlot.slot_id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    db.delete(slot)
    db.commit()
    return {"message": f"Slot {slot_id} deleted successfully"}
