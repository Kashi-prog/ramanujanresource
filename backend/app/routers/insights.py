"""Insights router - AI-generated recommendations and insights."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.database.models import Recommendation
from app.models.schemas import InsightResponse, EmissionStats, RecommendationResponse
from app.recommendations.engine import generate_recommendations
from app.routers.emissions import get_emission_stats

router = APIRouter()


@router.get("/", response_model=InsightResponse)
async def get_insights(
    user_id: int = Query(..., description="User ID"),
    days: int = Query(default=30, description="Number of days to look back"),
    db: Session = Depends(get_db)
):
    """Get comprehensive insights for a user."""
    # Get emission statistics
    stats = await get_emission_stats(user_id=user_id, days=days, db=db)
    
    # Generate or fetch recommendations
    recommendations = generate_recommendations(db, user_id, stats)
    
    # Calculate sustainability score (0-100, higher is better)
    # Score based on total emissions and trends
    avg_daily_co2 = stats.total_co2_grams / days if days > 0 else 0
    # Lower emissions = higher score
    # Using 500g CO2/day as a "good" benchmark
    sustainability_score = max(0, min(100, 100 - (avg_daily_co2 / 10)))
    
    return InsightResponse(
        user_id=user_id,
        period=f"{days} days",
        stats=stats,
        recommendations=[RecommendationResponse.model_validate(r) for r in recommendations],
        sustainability_score=round(sustainability_score, 1)
    )


@router.get("/recommendations")
async def list_recommendations(
    user_id: int = Query(..., description="User ID"),
    unread_only: bool = False,
    db: Session = Depends(get_db)
):
    """List recommendations for a user."""
    query = db.query(Recommendation).filter(Recommendation.user_id == user_id)
    
    if unread_only:
        query = query.filter(Recommendation.is_read == 0)
    
    recommendations = query.order_by(
        Recommendation.created_at.desc()
    ).limit(20).all()
    
    return {
        "recommendations": [
            RecommendationResponse.model_validate(r) for r in recommendations
        ]
    }


@router.put("/recommendations/{recommendation_id}/read")
async def mark_recommendation_read(
    recommendation_id: int,
    db: Session = Depends(get_db)
):
    """Mark a recommendation as read."""
    recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id
    ).first()
    
    if not recommendation:
        return {"error": "Recommendation not found"}
    
    recommendation.is_read = 1
    db.commit()
    
    return {"message": "Recommendation marked as read"}


@router.get("/tips")
async def get_daily_tips():
    """Get general sustainability tips."""
    tips = [
        {
            "category": "streaming",
            "tip": "Lower video quality when you don't need HD - it can reduce emissions by up to 80%",
            "impact": "high"
        },
        {
            "category": "browsing",
            "tip": "Use ad blockers to reduce unnecessary data transfer and energy use",
            "impact": "medium"
        },
        {
            "category": "cloud",
            "tip": "Regularly clean up old files and emails to reduce cloud storage energy",
            "impact": "medium"
        },
        {
            "category": "ai_query",
            "tip": "Batch your AI queries and use simpler models when possible",
            "impact": "high"
        },
        {
            "category": "general",
            "tip": "Enable dark mode on your devices to reduce screen energy consumption",
            "impact": "low"
        },
        {
            "category": "general",
            "tip": "Close unused browser tabs and applications to reduce CPU usage",
            "impact": "medium"
        }
    ]
    
    return {"tips": tips}
