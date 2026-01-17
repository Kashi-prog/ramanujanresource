"""Recommendation engine for personalized sustainability insights."""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.database.models import Recommendation
from app.models.schemas import EmissionStats


def generate_recommendations(
    db: Session,
    user_id: int,
    stats: EmissionStats
) -> List[Recommendation]:
    """Generate personalized recommendations based on user's emission stats."""
    recommendations = []
    
    # Get existing recommendations to avoid duplicates
    existing = db.query(Recommendation).filter(
        Recommendation.user_id == user_id
    ).order_by(Recommendation.created_at.desc()).limit(10).all()
    
    existing_texts = {r.recommendation_text for r in existing}
    
    # Analyze breakdown and generate recommendations
    if stats.breakdown_by_type:
        # Sort by highest emissions
        sorted_activities = sorted(
            stats.breakdown_by_type.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Streaming recommendations
        if "streaming" in stats.breakdown_by_type:
            streaming_co2 = stats.breakdown_by_type["streaming"]
            if streaming_co2 > 500:  # High streaming emissions
                rec_text = "Consider lowering video quality to 720p or 480p when high definition isn't necessary. This can reduce streaming emissions by up to 80%."
                if rec_text not in existing_texts:
                    recommendations.append(Recommendation(
                        user_id=user_id,
                        recommendation_text=rec_text,
                        category="streaming",
                        potential_savings_gco2=streaming_co2 * 0.5
                    ))
                
                rec_text = "Download videos on WiFi to watch offline instead of streaming repeatedly. This reduces redundant data transfer."
                if rec_text not in existing_texts:
                    recommendations.append(Recommendation(
                        user_id=user_id,
                        recommendation_text=rec_text,
                        category="streaming",
                        potential_savings_gco2=streaming_co2 * 0.3
                    ))
        
        # AI query recommendations
        if "ai_query" in stats.breakdown_by_type:
            ai_co2 = stats.breakdown_by_type["ai_query"]
            if ai_co2 > 300:
                rec_text = "Batch your AI queries together and be more specific in your prompts to reduce the number of iterations needed."
                if rec_text not in existing_texts:
                    recommendations.append(Recommendation(
                        user_id=user_id,
                        recommendation_text=rec_text,
                        category="ai_query",
                        potential_savings_gco2=ai_co2 * 0.4
                    ))
        
        # Cloud storage recommendations
        if "cloud" in stats.breakdown_by_type:
            cloud_co2 = stats.breakdown_by_type["cloud"]
            if cloud_co2 > 200:
                rec_text = "Regularly clean up duplicate files and old emails. Every GB of cloud storage that's actively maintained uses energy."
                if rec_text not in existing_texts:
                    recommendations.append(Recommendation(
                        user_id=user_id,
                        recommendation_text=rec_text,
                        category="cloud",
                        potential_savings_gco2=cloud_co2 * 0.25
                    ))
        
        # Browsing recommendations
        if "browsing" in stats.breakdown_by_type:
            browsing_co2 = stats.breakdown_by_type["browsing"]
            if browsing_co2 > 400:
                rec_text = "Use ad blockers and privacy extensions to reduce unnecessary data loading and tracking scripts."
                if rec_text not in existing_texts:
                    recommendations.append(Recommendation(
                        user_id=user_id,
                        recommendation_text=rec_text,
                        category="browsing",
                        potential_savings_gco2=browsing_co2 * 0.2
                    ))
    
    # General recommendations based on total emissions
    if stats.total_co2_grams > 2000:
        rec_text = "Your digital carbon footprint is above average. Consider using lower power modes and closing unused applications."
        if rec_text not in existing_texts:
            recommendations.append(Recommendation(
                user_id=user_id,
                recommendation_text=rec_text,
                category="general",
                potential_savings_gco2=stats.total_co2_grams * 0.15
            ))
    
    # Time-based recommendations
    rec_text = "Schedule large downloads and uploads for off-peak hours (10 PM - 6 AM) when the grid is cleaner."
    if rec_text not in existing_texts and stats.total_co2_grams > 1000:
        recommendations.append(Recommendation(
            user_id=user_id,
            recommendation_text=rec_text,
            category="general",
            potential_savings_gco2=stats.total_co2_grams * 0.1
        ))
    
    # Device recommendations
    rec_text = "Use mobile devices for light tasks - they consume significantly less energy than laptops or desktops."
    if rec_text not in existing_texts and stats.total_co2_grams > 1500:
        recommendations.append(Recommendation(
            user_id=user_id,
            recommendation_text=rec_text,
            category="general",
            potential_savings_gco2=stats.total_co2_grams * 0.12
        ))
    
    # Save new recommendations
    for rec in recommendations:
        db.add(rec)
    
    if recommendations:
        db.commit()
        for rec in recommendations:
            db.refresh(rec)
    
    # Return recent recommendations (including newly created ones)
    all_recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == user_id
    ).order_by(Recommendation.created_at.desc()).limit(10).all()
    
    return all_recommendations


def calculate_sustainability_score(
    total_co2_grams: float,
    total_activities: int,
    days: int
) -> float:
    """Calculate a sustainability score (0-100, higher is better)."""
    if days == 0:
        return 50.0
    
    avg_daily_co2 = total_co2_grams / days
    
    # Scoring thresholds
    # Excellent: < 300g/day = 90-100
    # Good: 300-500g/day = 70-90
    # Average: 500-800g/day = 50-70
    # Poor: 800-1200g/day = 30-50
    # Very Poor: > 1200g/day = 0-30
    
    if avg_daily_co2 < 300:
        score = 90 + (300 - avg_daily_co2) / 30
    elif avg_daily_co2 < 500:
        score = 70 + (500 - avg_daily_co2) / 10
    elif avg_daily_co2 < 800:
        score = 50 + (800 - avg_daily_co2) / 15
    elif avg_daily_co2 < 1200:
        score = 30 + (1200 - avg_daily_co2) / 20
    else:
        score = max(0, 30 - (avg_daily_co2 - 1200) / 40)
    
    return round(min(100, max(0, score)), 1)
