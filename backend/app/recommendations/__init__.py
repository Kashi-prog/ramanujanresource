"""Recommendations module."""

from app.recommendations.engine import generate_recommendations, calculate_sustainability_score

__all__ = ["generate_recommendations", "calculate_sustainability_score"]
