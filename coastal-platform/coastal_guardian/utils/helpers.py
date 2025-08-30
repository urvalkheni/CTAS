import pandas as pd
import json
import os
from datetime import datetime
import numpy as np

def load_coastal_data(file_path=None):
    """Load coastal data from CSV file"""
    if file_path is None:
        file_path = "data/sample.csv"
    
    try:
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def analyze_threats(df):
    """Analyze coastal data for threats"""
    alerts = []
    
    if df is None or df.empty:
        return alerts
    
    # High tide alert
    if df["tide_level"].iloc[-1] > 3.5:
        alerts.append({
            "type": "High Tide",
            "severity": "High",
            "message": f"🚨 High Tide Alert! Current level: {df['tide_level'].iloc[-1]:.1f}m",
            "location": df["location"].iloc[-1]
        })
    
    # High sea level alert
    if df["sea_level"].iloc[-1] > 1.5:
        alerts.append({
            "type": "High Sea Level",
            "severity": "Medium",
            "message": f"⚠️ Elevated Sea Level! Current: {df['sea_level'].iloc[-1]:.1f}m",
            "location": df["location"].iloc[-1]
        })
    
    # High wave alert
    if df["wave_height"].iloc[-1] > 2.5:
        alerts.append({
            "type": "High Waves",
            "severity": "Medium",
            "message": f"🌊 High Wave Alert! Height: {df['wave_height'].iloc[-1]:.1f}m",
            "location": df["location"].iloc[-1]
        })
    
    return alerts

def load_contributions():
    """Load user contributions from JSON"""
    try:
        with open("reports/contributions.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"reports": []}

def save_contribution(user, location, status, confidence=80):
    """Save new contribution to JSON"""
    contributions = load_contributions()
    
    # Calculate points based on status
    points = 50 if status == "healthy" else 25
    
    new_report = {
        "user": user,
        "location": location,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "points": points,
        "status": status,
        "confidence": confidence
    }
    
    contributions["reports"].append(new_report)
    
    with open("reports/contributions.json", "w") as f:
        json.dump(contributions, f, indent=2)
    
    return new_report

def analyze_mangrove_image(filename):
    """Mock AI analysis of mangrove image"""
    # Simple mock analysis based on filename
    if "cut" in filename.lower():
        return "cut", 85
    elif "healthy" in filename.lower():
        return "healthy", 90
    else:
        # Random analysis for demo
        import random
        status = random.choice(["healthy", "cut"])
        confidence = random.randint(75, 95)
        return status, confidence

def get_leaderboard():
    """Get user leaderboard from contributions"""
    contributions = load_contributions()
    
    if not contributions["reports"]:
        return pd.DataFrame()
    
    # Group by user and sum points
    user_points = {}
    for report in contributions["reports"]:
        user = report["user"]
        points = report["points"]
        user_points[user] = user_points.get(user, 0) + points
    
    # Convert to DataFrame
    leaderboard = pd.DataFrame([
        {"user": user, "points": points} 
        for user, points in user_points.items()
    ])
    
    return leaderboard.sort_values("points", ascending=False)

def get_coastal_locations():
    """Get coastal locations for mapping"""
    return [
        {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
        {"name": "Goa", "lat": 15.2993, "lon": 74.1240},
        {"name": "Chennai", "lat": 13.0827, "lon": 80.2707},
        {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639},
        {"name": "Kochi", "lat": 9.9312, "lon": 76.2673}
    ]
