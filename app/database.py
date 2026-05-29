# SQL Alchemy - Object relational mapper, turns python code into sql database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv
import os

load_dotenv()   #   loads .env credentials

DATABASE_URL = os.getenv("DATABASE_URL")    #gets the database url

Base = declarative_base()   #   defines which tables exist and how they look
engine = create_engine(DATABASE_URL)    #   connects (lazy initialitation)
SessionLocal = sessionmaker(bind=engine)    # create sessions for the operations

def get_db():
    """Yields a DB session and guarantees it closes, even on error."""
    db = SessionLocal()
    try:
        yield db  # pauses here — caller uses db, then Python runs finally
    finally:
        db.close()