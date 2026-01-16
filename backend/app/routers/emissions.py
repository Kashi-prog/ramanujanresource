"""Emissions router - Carbon emission calculations and statistics."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Dict

from app.database import get_db
from app.database.models import Activity, Emission
from app.models.schemas import EmissionStats

router = APIRouter()


@router.get("/stats", response_model=EmissionStats)
async def get_emission_stats(
    user_id: int = Query(..., description="User ID"),
    days: int = Query(default=30, description="Number of days to look back"),
    db: Session = Depends(get_db)
):
    """Get emission statistics for a user."""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Query emissions with activities
    emissions = db.query(Emission, Activity).join(
        Activity, Activity.id == Emission.activity_id
    ).filter(
        Activity.user_id == user_id,
        Activity.timestamp >= cutoff_date
    ).all()
    
    if not emissions:
        return EmissionStats(
            total_co2_grams=0.0,
            total_activities=0,
            average_co2_per_activity=0.0,
            breakdown_by_type={}
        )
    
    # Calculate statistics
    total_co2 = sum(e.co2_grams for e, _ in emissions)
    total_activities = len(emissions)
    average_co2 = total_co2 / total_activities if total_activities > 0 else 0.0
    
    # Breakdown by activity type
    breakdown: Dict[str, float] = {}
    for emission, activity in emissions:
        activity_type = activity.activity_type
        breakdown[activity_type] = breakdown.get(activity_type, 0.0) + emission.co2_grams
    
    return EmissionStats(
        total_co2_grams=round(total_co2, 2),
        total_activities=total_activities,
        average_co2_per_activity=round(average_co2, 2),
        breakdown_by_type=breakdown
    )


@router.get("/timeline")
async def get_emission_timeline(
    user_id: int = Query(..., description="User ID"),
    days: int = Query(default=30, description="Number of days to look back"),
    db: Session = Depends(get_db)
):
    """Get daily emission timeline for visualization."""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Query emissions grouped by date
    results = db.query(
        func.date(Activity.timestamp).label("date"),
        func.sum(Emission.co2_grams).label("total_co2")
    ).join(
        Activity, Activity.id == Emission.activity_id
    ).filter(
        Activity.user_id == user_id,
        Activity.timestamp >= cutoff_date
    ).group_by(
        func.date(Activity.timestamp)
    ).order_by(
        func.date(Activity.timestamp)
    ).all()
    
    timeline = [
        {
            "date": str(result.date),
            "co2_grams": round(result.total_co2, 2)
        }
        for result in results
    ]
    
    return {"timeline": timeline}


@router.get("/comparison")
async def get_emission_comparison(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Compare user's emissions with averages."""
    # Get user's total emissions
    user_emissions = db.query(func.sum(Emission.co2_grams)).join(
        Activity, Activity.id == Emission.activity_id
    ).filter(Activity.user_id == user_id).scalar() or 0.0
    
    # Get average emissions across all users
    avg_emissions = db.query(func.avg(Emission.co2_grams)).scalar() or 0.0
    
    # Calculate percentile (simplified)
    all_user_totals = db.query(
        Activity.user_id,
        func.sum(Emission.co2_grams).label("total")
    ).join(
        Emission, Activity.id == Emission.activity_id
    ).group_by(Activity.user_id).all()
    
    if all_user_totals:
        sorted_totals = sorted([t.total for t in all_user_totals])
        user_rank = sum(1 for t in sorted_totals if t < user_emissions)
        percentile = (user_rank / len(sorted_totals)) * 100 if sorted_totals else 50
    else:
        percentile = 50
    
    return {
        "user_total_co2": round(user_emissions, 2),
        "global_average_co2": round(avg_emissions * len(all_user_totals) if all_user_totals else 0, 2),
        "percentile": round(percentile, 1),
        "message": f"You are in the {round(percentile)}th percentile"
    }
