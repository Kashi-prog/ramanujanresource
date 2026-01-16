"""Carbon emission estimation model."""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict

from app.database.models import Activity, Emission
from app.config import settings


# Energy consumption factors (kWh per unit)
ENERGY_FACTORS = {
    "streaming": {
        "laptop": 0.05,      # kWh per hour for HD streaming on laptop
        "desktop": 0.08,     # kWh per hour for HD streaming on desktop
        "mobile": 0.015,     # kWh per hour for streaming on mobile
    },
    "browsing": {
        "laptop": 0.02,      # kWh per hour for web browsing on laptop
        "desktop": 0.035,    # kWh per hour for web browsing on desktop
        "mobile": 0.008,     # kWh per hour for browsing on mobile
    },
    "cloud": {
        "laptop": 0.001,     # kWh per MB of cloud storage/transfer
        "desktop": 0.001,    # Same for all devices (mostly server-side)
        "mobile": 0.001,
    },
    "ai_query": {
        "laptop": 0.1,       # kWh per hour of AI usage
        "desktop": 0.12,     # kWh per hour of AI usage
        "mobile": 0.03,      # kWh per hour of AI usage on mobile
    }
}

# Regional carbon intensity (gCO2/kWh)
CARBON_INTENSITY = {
    "Global": 475.0,
    "US": 385.0,
    "Europe": 295.0,
    "Asia": 550.0,
    "Nordic": 85.0,
    "UK": 233.0,
    "Australia": 650.0,
    "Canada": 130.0,
    "India": 630.0,
    "China": 555.0,
}


def get_carbon_intensity(region: str) -> float:
    """Get carbon intensity for a region."""
    return CARBON_INTENSITY.get(region, settings.default_carbon_intensity)


def calculate_energy_consumption(
    activity_type: str,
    duration_minutes: float,
    device_type: str,
    data_volume_mb: float = 0.0
) -> float:
    """Calculate energy consumption for an activity."""
    if activity_type not in ENERGY_FACTORS:
        # Default to browsing for unknown types
        activity_type = "browsing"
    
    device_factors = ENERGY_FACTORS[activity_type]
    energy_per_hour = device_factors.get(device_type, device_factors.get("laptop", 0.02))
    
    # Calculate base energy from duration
    duration_hours = duration_minutes / 60.0
    base_energy = energy_per_hour * duration_hours
    
    # Add data transfer energy for cloud activities
    if activity_type == "cloud" and data_volume_mb > 0:
        data_energy = ENERGY_FACTORS["cloud"]["laptop"] * data_volume_mb
        base_energy += data_energy
    
    return base_energy


def apply_contextual_factors(
    base_energy: float,
    timestamp: datetime
) -> float:
    """Apply contextual factors like time of day."""
    # Night time (10 PM - 6 AM) typically has lower carbon intensity
    hour = timestamp.hour
    if 22 <= hour or hour < 6:
        # 10% reduction for night time usage
        return base_energy * 0.9
    
    # Peak hours (5 PM - 9 PM) might have higher intensity
    elif 17 <= hour < 21:
        # 5% increase for peak hours
        return base_energy * 1.05
    
    return base_energy


def estimate_emissions(
    db: Session,
    activity: Activity,
    region: str = "Global"
) -> Emission:
    """Estimate carbon emissions for an activity."""
    # Calculate base energy consumption
    base_energy = calculate_energy_consumption(
        activity.activity_type,
        activity.duration_minutes,
        activity.device_type,
        activity.data_volume_mb
    )
    
    # Apply contextual factors
    adjusted_energy = apply_contextual_factors(base_energy, activity.timestamp)
    
    # Get carbon intensity for region
    carbon_intensity = get_carbon_intensity(region)
    
    # Calculate CO2 emissions
    co2_grams = adjusted_energy * carbon_intensity
    
    # Create or update emission record
    existing_emission = db.query(Emission).filter(
        Emission.activity_id == activity.id
    ).first()
    
    if existing_emission:
        existing_emission.energy_kwh = adjusted_energy
        existing_emission.carbon_intensity = carbon_intensity
        existing_emission.co2_grams = co2_grams
        existing_emission.calculation_timestamp = datetime.utcnow()
        emission = existing_emission
    else:
        emission = Emission(
            activity_id=activity.id,
            energy_kwh=adjusted_energy,
            carbon_intensity=carbon_intensity,
            co2_grams=co2_grams
        )
        db.add(emission)
    
    db.commit()
    db.refresh(emission)
    
    return emission


def predict_future_emissions(
    historical_activities: list,
    days_ahead: int = 7
) -> Dict[str, float]:
    """Predict future emissions based on historical data."""
    if not historical_activities:
        return {"prediction": 0.0, "confidence": 0.0}
    
    # Simple average-based prediction
    total_co2 = sum(
        activity.emission.co2_grams 
        for activity in historical_activities 
        if activity.emission
    )
    
    days_of_data = len(set(activity.timestamp.date() for activity in historical_activities))
    
    if days_of_data == 0:
        return {"prediction": 0.0, "confidence": 0.0}
    
    daily_average = total_co2 / days_of_data
    predicted_total = daily_average * days_ahead
    
    # Confidence based on amount of historical data
    confidence = min(1.0, days_of_data / 30.0)
    
    return {
        "prediction": round(predicted_total, 2),
        "daily_average": round(daily_average, 2),
        "confidence": round(confidence * 100, 1)
    }
