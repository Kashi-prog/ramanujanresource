"""Activities router - CRUD operations for digital activities."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.database import get_db
from app.database.models import Activity, User
from app.models.schemas import ActivityCreate, ActivityResponse, ActivityWithEmission
from app.ml.estimator import estimate_emissions

router = APIRouter()


@router.post("/", response_model=ActivityResponse, status_code=201)
async def create_activity(
    activity: ActivityCreate,
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Create a new digital activity and calculate its emissions."""
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create activity
    db_activity = Activity(
        user_id=user_id,
        **activity.model_dump()
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    # Calculate emissions
    try:
        estimate_emissions(db, db_activity, user.region)
    except Exception as e:
        print(f"Error calculating emissions: {e}")
    
    return db_activity


@router.get("/", response_model=List[ActivityWithEmission])
async def list_activities(
    user_id: int = Query(..., description="User ID"),
    skip: int = 0,
    limit: int = 100,
    days: int = Query(default=30, description="Number of days to look back"),
    db: Session = Depends(get_db)
):
    """List activities for a user."""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    activities = db.query(Activity).filter(
        Activity.user_id == user_id,
        Activity.timestamp >= cutoff_date
    ).order_by(Activity.timestamp.desc()).offset(skip).limit(limit).all()
    
    # Enrich with emission data
    result = []
    for activity in activities:
        activity_dict = ActivityWithEmission.model_validate(activity).model_dump()
        if activity.emission:
            activity_dict["co2_grams"] = activity.emission.co2_grams
            activity_dict["energy_kwh"] = activity.emission.energy_kwh
        result.append(ActivityWithEmission(**activity_dict))
    
    return result


@router.get("/{activity_id}", response_model=ActivityWithEmission)
async def get_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific activity by ID."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity_dict = ActivityWithEmission.model_validate(activity).model_dump()
    if activity.emission:
        activity_dict["co2_grams"] = activity.emission.co2_grams
        activity_dict["energy_kwh"] = activity.emission.energy_kwh
    
    return ActivityWithEmission(**activity_dict)


@router.delete("/{activity_id}")
async def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    """Delete an activity."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    db.delete(activity)
    db.commit()
    
    return {"message": "Activity deleted successfully"}
