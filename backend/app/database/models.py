"""Database models for Carbon Shadow Tracker."""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    region = Column(String, default="Global")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    activities = relationship("Activity", back_populates="user")


class Activity(Base):
    """Digital activity model."""
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_type = Column(String, nullable=False)  # streaming, browsing, cloud, ai_query
    duration_minutes = Column(Float, nullable=False)
    data_volume_mb = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    device_type = Column(String, default="laptop")  # laptop, mobile, desktop
    
    user = relationship("User", back_populates="activities")
    emission = relationship("Emission", back_populates="activity", uselist=False)


class Emission(Base):
    """Carbon emission calculation model."""
    __tablename__ = "emissions"
    
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False, unique=True)
    energy_kwh = Column(Float, nullable=False)
    carbon_intensity = Column(Float, nullable=False)  # gCO2/kWh
    co2_grams = Column(Float, nullable=False)
    calculation_timestamp = Column(DateTime, default=datetime.utcnow)
    
    activity = relationship("Activity", back_populates="emission")


class Recommendation(Base):
    """User recommendations model."""
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recommendation_text = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    potential_savings_gco2 = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Integer, default=0)  # SQLite doesn't have boolean
