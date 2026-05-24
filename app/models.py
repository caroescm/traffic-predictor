from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from app.database import Base

class TravelQuery(Base):
    __tablename__ = "travel_queries"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    origin = Column(String)
    destination = Column(String)
    duration_minutes = Column(Float)
    weather = Column(String)
    temperature = Column(Float)
    is_holiday = Column(Boolean)
    day_of_week = Column(String)
    queried_at = Column(DateTime)