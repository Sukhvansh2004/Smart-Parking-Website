from sqlalchemy import create_engine, Column, String, Boolean, Date, Time, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from secret import DATABASE_URL  # Import from secrets.py

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    slot_id = Column(String, ForeignKey("parking_slots.slot_id"))
    user_email = Column(String)
    booking_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)

class ParkingSlot(Base):
    __tablename__ = "parking_slots"
    slot_id = Column(String, primary_key=True, index=True)
    status = Column(Boolean, default=True)

class Admin(Base):
    __tablename__ = "admins"
    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)
