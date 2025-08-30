#!/usr/bin/env python3
"""
Simple test script to verify the API endpoints are working.
"""

import requests
import json
import time

def test_api():
    """Test the API endpoints."""
    base_url = "http://localhost:8000"
    
    print("🚀 Testing Coastal Guardian ML Anomaly Detection API")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: Root endpoint
    print("\n2. Testing Root Endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            print(f"API Info: {response.json()}")
        else:
            print(f"❌ Root endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    # Test 3: Storm surge prediction
    print("\n3. Testing Storm Surge Prediction...")
    try:
        data = {
            "sea_level": 3.5,
            "wind_speed": 45.0,
            "atmospheric_pressure": 985.0,
            "wave_height": 4.2
        }
        response = requests.post(f"{base_url}/storm-surge/predict", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Storm surge prediction working!")
            print(f"Prediction: {result['is_anomaly']}")
            print(f"Threat Level: {result['threat_level']}")
            print(f"Recommendations: {result['recommendations']}")
        else:
            print(f"❌ Storm surge prediction failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Storm surge prediction failed: {e}")
    
    # Test 4: Water quality prediction
    print("\n4. Testing Water Quality Prediction...")
    try:
        data = {
            "ph": 5.2,
            "turbidity": 25.0,
            "dissolved_oxygen": 3.0,
            "temperature": 32.0,
            "conductivity": 1200.0
        }
        response = requests.post(f"{base_url}/water-quality/predict", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Water quality prediction working!")
            print(f"Prediction: {result['is_anomaly']}")
            print(f"Threat Level: {result['threat_level']}")
            print(f"Recommendations: {result['recommendations']}")
        else:
            print(f"❌ Water quality prediction failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Water quality prediction failed: {e}")
    
    # Test 5: General prediction
    print("\n5. Testing General Prediction...")
    try:
        data = {
            "sea_level": 2.8,
            "wind_speed": 35.0,
            "ph": 6.8,
            "temperature": 28.0
        }
        response = requests.post(f"{base_url}/predict", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ General prediction working!")
            print(f"Prediction: {result['is_anomaly']}")
            print(f"Threat Level: {result['threat_level']}")
        else:
            print(f"❌ General prediction failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ General prediction failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 API Testing Complete!")
    print(f"📖 API Documentation available at: {base_url}/docs")
    print(f"🔧 Interactive API docs at: {base_url}/redoc")

if __name__ == "__main__":
    # Wait a moment for the server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    test_api()
