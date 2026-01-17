"""Data collectors for simulating and collecting digital activity data."""

from typing import Dict, List
from datetime import datetime, timedelta
import random


class ActivityCollector:
    """Base class for activity data collection."""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
    
    def collect(self) -> List[Dict]:
        """Collect activity data."""
        raise NotImplementedError


class StreamingCollector(ActivityCollector):
    """Collector for streaming activity data."""
    
    def generate_sample_data(self, days: int = 7) -> List[Dict]:
        """Generate sample streaming data."""
        activities = []
        
        for day in range(days):
            # Simulate 1-3 streaming sessions per day
            sessions = random.randint(1, 3)
            
            for _ in range(sessions):
                timestamp = datetime.utcnow() - timedelta(
                    days=day,
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                activities.append({
                    "activity_type": "streaming",
                    "duration_minutes": random.uniform(15, 180),
                    "data_volume_mb": random.uniform(500, 3000),
                    "device_type": random.choice(["laptop", "mobile", "desktop"]),
                    "timestamp": timestamp
                })
        
        return activities


class BrowsingCollector(ActivityCollector):
    """Collector for web browsing activity data."""
    
    def generate_sample_data(self, days: int = 7) -> List[Dict]:
        """Generate sample browsing data."""
        activities = []
        
        for day in range(days):
            # Simulate 3-8 browsing sessions per day
            sessions = random.randint(3, 8)
            
            for _ in range(sessions):
                timestamp = datetime.utcnow() - timedelta(
                    days=day,
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                activities.append({
                    "activity_type": "browsing",
                    "duration_minutes": random.uniform(5, 120),
                    "data_volume_mb": random.uniform(50, 500),
                    "device_type": random.choice(["laptop", "mobile", "desktop"]),
                    "timestamp": timestamp
                })
        
        return activities


class CloudCollector(ActivityCollector):
    """Collector for cloud storage activity data."""
    
    def generate_sample_data(self, days: int = 7) -> List[Dict]:
        """Generate sample cloud activity data."""
        activities = []
        
        for day in range(days):
            # Simulate 0-3 cloud operations per day
            operations = random.randint(0, 3)
            
            for _ in range(operations):
                timestamp = datetime.utcnow() - timedelta(
                    days=day,
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                activities.append({
                    "activity_type": "cloud",
                    "duration_minutes": random.uniform(1, 30),
                    "data_volume_mb": random.uniform(10, 5000),
                    "device_type": random.choice(["laptop", "mobile", "desktop"]),
                    "timestamp": timestamp
                })
        
        return activities


class AIQueryCollector(ActivityCollector):
    """Collector for AI query activity data."""
    
    def generate_sample_data(self, days: int = 7) -> List[Dict]:
        """Generate sample AI query data."""
        activities = []
        
        for day in range(days):
            # Simulate 0-5 AI query sessions per day
            sessions = random.randint(0, 5)
            
            for _ in range(sessions):
                timestamp = datetime.utcnow() - timedelta(
                    days=day,
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                activities.append({
                    "activity_type": "ai_query",
                    "duration_minutes": random.uniform(2, 30),
                    "data_volume_mb": random.uniform(1, 50),
                    "device_type": random.choice(["laptop", "mobile", "desktop"]),
                    "timestamp": timestamp
                })
        
        return activities


def generate_sample_activities(user_id: int, days: int = 7) -> List[Dict]:
    """Generate sample activities for testing."""
    streaming = StreamingCollector(user_id)
    browsing = BrowsingCollector(user_id)
    cloud = CloudCollector(user_id)
    ai_query = AIQueryCollector(user_id)
    
    all_activities = []
    all_activities.extend(streaming.generate_sample_data(days))
    all_activities.extend(browsing.generate_sample_data(days))
    all_activities.extend(cloud.generate_sample_data(days))
    all_activities.extend(ai_query.generate_sample_data(days))
    
    # Sort by timestamp
    all_activities.sort(key=lambda x: x["timestamp"])
    
    return all_activities
