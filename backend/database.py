from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update this with your actual PostgreSQL credentials:
DATABASE_URL = "postgresql://sukhvansh:210204@localhost/smart_parking"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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
