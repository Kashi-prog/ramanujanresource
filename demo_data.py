"""
Demo script to populate the Carbon Shadow Tracker with sample data.
This script creates a demo user and adds various activities to showcase the application.
"""

import requests
import random
from datetime import datetime, timedelta
import time

# API Configuration
BASE_URL = "http://localhost:8000/api/v1"

def create_user():
    """Create a demo user."""
    print("Creating demo user...")
    
    user_data = {
        "email": "demo@carbonshadow.com",
        "username": "demo_user",
        "password": "demo123",
        "region": "US"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    
    if response.status_code == 201:
        user = response.json()
        print(f"✓ Created user: {user['username']} (ID: {user['id']})")
        return user['id']
    elif response.status_code == 400 and "already exists" in response.text:
        # User already exists, fetch it
        response = requests.get(f"{BASE_URL}/users/username/demo_user")
        user = response.json()
        print(f"✓ Using existing user: {user['username']} (ID: {user['id']})")
        return user['id']
    else:
        print(f"✗ Failed to create user: {response.text}")
        return None

def add_activity(user_id, activity_type, duration, data_volume, device_type):
    """Add an activity for the user."""
    activity_data = {
        "activity_type": activity_type,
        "duration_minutes": duration,
        "data_volume_mb": data_volume,
        "device_type": device_type
    }
    
    response = requests.post(
        f"{BASE_URL}/activities/?user_id={user_id}",
        json=activity_data
    )
    
    if response.status_code == 201:
        activity = response.json()
        print(f"  ✓ Added {activity_type}: {duration} min, {device_type}")
        return activity
    else:
        print(f"  ✗ Failed to add activity: {response.text}")
        return None

def generate_sample_activities(user_id):
    """Generate sample activities for the demo."""
    print("\nGenerating sample activities...")
    
    activities = [
        # Streaming activities
        ("streaming", 120, 2500, "laptop"),
        ("streaming", 45, 800, "mobile"),
        ("streaming", 90, 1800, "desktop"),
        ("streaming", 60, 1200, "laptop"),
        
        # Browsing activities
        ("browsing", 180, 400, "laptop"),
        ("browsing", 30, 80, "mobile"),
        ("browsing", 120, 250, "desktop"),
        ("browsing", 90, 180, "laptop"),
        ("browsing", 45, 100, "mobile"),
        
        # Cloud activities
        ("cloud", 15, 5000, "laptop"),
        ("cloud", 8, 2500, "desktop"),
        ("cloud", 5, 1000, "mobile"),
        
        # AI query activities
        ("ai_query", 25, 30, "laptop"),
        ("ai_query", 15, 20, "desktop"),
        ("ai_query", 10, 15, "laptop"),
        ("ai_query", 20, 25, "mobile"),
    ]
    
    for activity in activities:
        add_activity(user_id, *activity)
        time.sleep(0.1)  # Small delay to avoid overwhelming the API
    
    print(f"\n✓ Added {len(activities)} sample activities")

def display_stats(user_id):
    """Display emission statistics."""
    print("\n" + "="*60)
    print("EMISSION STATISTICS")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/emissions/stats?user_id={user_id}")
    if response.status_code == 200:
        stats = response.json()
        print(f"\nTotal CO₂ Emissions: {stats['total_co2_grams']/1000:.2f} kg")
        print(f"Total Activities: {stats['total_activities']}")
        print(f"Average per Activity: {stats['average_co2_per_activity']:.2f} g CO₂")
        
        print("\nBreakdown by Type:")
        for activity_type, co2 in stats['breakdown_by_type'].items():
            print(f"  {activity_type.upper()}: {co2:.2f} g CO₂")
    
    # Get insights
    response = requests.get(f"{BASE_URL}/insights/?user_id={user_id}")
    if response.status_code == 200:
        insights = response.json()
        print(f"\nSustainability Score: {insights['sustainability_score']}/100")
        
        if insights['recommendations']:
            print(f"\nRecommendations ({len(insights['recommendations'])} total):")
            for i, rec in enumerate(insights['recommendations'][:3], 1):
                print(f"\n  {i}. [{rec['category'].upper()}]")
                print(f"     {rec['recommendation_text']}")
                print(f"     💚 Potential savings: {rec['potential_savings_gco2']/1000:.2f} kg CO₂")

def main():
    """Main demo script."""
    print("="*60)
    print("Carbon Shadow Tracker - Demo Data Generator")
    print("="*60)
    
    try:
        # Check if API is running
        response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health")
        if response.status_code != 200:
            print("\n✗ API is not responding. Please start the backend first:")
            print("  cd backend && uvicorn app.main:app --reload")
            return
    except requests.exceptions.ConnectionError:
        print("\n✗ Cannot connect to API. Please start the backend first:")
        print("  cd backend && uvicorn app.main:app --reload")
        return
    
    # Create user
    user_id = create_user()
    if not user_id:
        return
    
    # Generate activities
    generate_sample_activities(user_id)
    
    # Display statistics
    display_stats(user_id)
    
    print("\n" + "="*60)
    print("Demo data generation complete!")
    print("="*60)
    print("\nYou can now:")
    print("  1. Open the frontend: http://localhost:3000")
    print("  2. View API docs: http://localhost:8000/docs")
    print("  3. Explore the dashboard with sample data")
    print("\nHappy tracking! 🌱")

if __name__ == "__main__":
    main()
