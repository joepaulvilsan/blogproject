import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv  # <-- Import this

# This line reads your .env file and loads the variables
load_dotenv()

# Get the database URL from the environment
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

# --- IMPORTANT ---
# For local dev, your .env file's DATABASE_URL should point to localhost:5433
# For Docker, it should point to db:5432
# You might need to change this one line in your .env file 
# depending on how you are running the app.

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
