import pandas as pd
import random
import time
import numpy as np
import requests

# Simulate tide sensor data
def generate_tide_data():
    return {
        "timestamp": pd.Timestamp.now().isoformat(),
        "tide_level": round(random.uniform(0.5, 4.0), 2),  # meters
        "wave_height": round(random.uniform(0.2, 3.5), 2), # meters
        "wind_speed": round(random.uniform(5, 60), 2)      # km/h
    }

# Simulate weather station data
def generate_weather_data():
    return {
        "timestamp": pd.Timestamp.now().isoformat(),
        "temperature": round(random.uniform(15, 35), 2),   # Celsius
        "humidity": round(random.uniform(40, 90), 2),      # %
        "precipitation": round(random.uniform(0, 20), 2)   # mm
    }

# Download or generate historical dataset
def generate_historical_data():
    data = []
    for i in range(100):
        data.append({
            "timestamp": (pd.Timestamp.now() - pd.Timedelta(days=i)).isoformat(),
            "tide_level": round(random.uniform(0.5, 4.0), 2),
            "wave_height": round(random.uniform(0.2, 3.5), 2),
            "wind_speed": round(random.uniform(5, 60), 2)
        })
    df = pd.DataFrame(data)
    df.to_csv("data/historical_tide_data.csv", index=False)
    print("✅ Historical data generated and saved.")

# Simulate satellite/API feed (dummy NOAA/NASA)
def fetch_satellite_data():
    # Simulate API response
    data = []
    for i in range(50):
        data.append({
            "timestamp": (pd.Timestamp.now() - pd.Timedelta(hours=i)).isoformat(),
            "sea_surface_temp": round(random.uniform(20, 32), 2), # Celsius
            "cyclone_alert": random.choice([0, 1])
        })
    df = pd.DataFrame(data)
    df.to_csv("data/simulated_satellite_data.csv", index=False)
    print("✅ Satellite data generated and saved.")

# Clean and preprocess data
def clean_and_preprocess(file_path):
    df = pd.read_csv(file_path)
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    # Normalize units if needed (example: wind_speed from km/h to m/s)
    if 'wind_speed' in df.columns:
        df['wind_speed'] = df['wind_speed'] * 0.27778
    df.to_csv(file_path, index=False)
    print(f"✅ Cleaned and preprocessed {file_path}.")

if __name__ == "__main__":
    # Simulate and save sensor data
    sensor_df = pd.DataFrame([generate_tide_data() for _ in range(100)])
    sensor_df.to_csv("data/simulated_tide_data.csv", index=False)
    print("✅ Sensor data generated and saved.")

    # Simulate and save weather station data
    weather_df = pd.DataFrame([generate_weather_data() for _ in range(100)])
    weather_df.to_csv("data/simulated_weather_data.csv", index=False)
    print("✅ Weather station data generated and saved.")

    # Generate and save historical data
    generate_historical_data()

    # Simulate and save satellite/API data
    fetch_satellite_data()

    # Clean and preprocess all generated files
    clean_and_preprocess("data/simulated_tide_data.csv")
    clean_and_preprocess("data/simulated_weather_data.csv")
    clean_and_preprocess("data/historical_tide_data.csv")
    clean_and_preprocess("data/simulated_satellite_data.csv")
