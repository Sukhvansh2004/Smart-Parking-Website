from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from datetime import date, time, timedelta
from database import SessionLocal, Booking, ParkingSlot  # Ensure Booking model exists in database.py
from auth import verify_google_token

router = APIRouter()

MAX_BOOKINGS_PER_DAY = 3      # Maximum slots a user can book per day
BOOKABLE_START = time(6, 0)     # 6 AM
BOOKABLE_END = time(23, 0)      # 11 PM

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/book")
def book_slot(
    slot_id: str,
    booking_date: date,
    start_time: time,
    end_time: time,
    google_token: str = Header(...),
    db: Session = Depends(get_db)
):
    # Verify Google token and extract user email
    user_info = verify_google_token(google_token)
    user_email = user_info.get("email")
    
    # Validate booking times
    if start_time < BOOKABLE_START or end_time > BOOKABLE_END:
        raise HTTPException(status_code=400, detail="Booking must be between 6 AM and 11 PM")
    if start_time >= end_time:
        raise HTTPException(status_code=400, detail="Start time must be before end time")
    
    # Allow advance booking only up to 2 days ahead
    if booking_date > date.today() + timedelta(days=2):
        raise HTTPException(status_code=400, detail="Bookings can only be made up to 2 days in advance")
    
    # Enforce user's daily booking limit
    user_bookings = db.query(Booking).filter(
        Booking.user_email == user_email,
        Booking.booking_date == booking_date
    ).count()
    if user_bookings >= MAX_BOOKINGS_PER_DAY:
        raise HTTPException(status_code=400, detail="You have reached your daily booking limit")
    
    # Check for overlapping bookings on the same slot
    overlapping = db.query(Booking).filter(
        Booking.slot_id == slot_id,
        Booking.booking_date == booking_date,
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).first()
    if overlapping:
        raise HTTPException(status_code=400, detail="The slot is already booked for the requested time interval")
    
    # Create new booking
    new_booking = Booking(
        slot_id=slot_id,
        user_email=user_email,
        booking_date=booking_date,
        start_time=start_time,
        end_time=end_time
    )
    db.add(new_booking)
    db.commit()
    return {"message": f"Slot {slot_id} booked successfully from {start_time} to {end_time} on {booking_date}"}
