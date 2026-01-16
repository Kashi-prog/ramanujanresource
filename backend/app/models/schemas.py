"""Pydantic models for request/response schemas."""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# User Schemas
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str
    region: str = "Global"


class UserCreate(UserBase):
    """User creation schema."""
    password: str


class UserResponse(UserBase):
    """User response schema."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Activity Schemas
class ActivityBase(BaseModel):
    """Base activity schema."""
    activity_type: str = Field(..., description="Type: streaming, browsing, cloud, ai_query")
    duration_minutes: float = Field(..., gt=0)
    data_volume_mb: float = Field(default=0.0, ge=0)
    device_type: str = Field(default="laptop")


class ActivityCreate(ActivityBase):
    """Activity creation schema."""
    pass


class ActivityResponse(ActivityBase):
    """Activity response schema."""
    id: int
    user_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ActivityWithEmission(ActivityResponse):
    """Activity with emission data."""
    co2_grams: Optional[float] = None
    energy_kwh: Optional[float] = None


# Emission Schemas
class EmissionBase(BaseModel):
    """Base emission schema."""
    energy_kwh: float
    carbon_intensity: float
    co2_grams: float


class EmissionResponse(EmissionBase):
    """Emission response schema."""
    id: int
    activity_id: int
    calculation_timestamp: datetime
    
    class Config:
        from_attributes = True


# Recommendation Schemas
class RecommendationBase(BaseModel):
    """Base recommendation schema."""
    recommendation_text: str
    category: str
    potential_savings_gco2: float = 0.0


class RecommendationResponse(RecommendationBase):
    """Recommendation response schema."""
    id: int
    user_id: int
    created_at: datetime
    is_read: bool
    
    class Config:
        from_attributes = True


# Statistics Schemas
class EmissionStats(BaseModel):
    """Emission statistics schema."""
    total_co2_grams: float
    total_activities: int
    average_co2_per_activity: float
    breakdown_by_type: dict


class InsightResponse(BaseModel):
    """Insight response schema."""
    user_id: int
    period: str
    stats: EmissionStats
    recommendations: list[RecommendationResponse]
    sustainability_score: float
