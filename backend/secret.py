import os

# Database credentials
DATABASE_URL = os.getenv("DATABASE_URL")

# FastAPI JWT Secret Key (change this to a strong, random value in production)
SECRET_KEY = os.getenv("SECRET_KEY")

# Google OAuth Credentials
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
