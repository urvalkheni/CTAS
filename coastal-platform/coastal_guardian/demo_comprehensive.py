#!/usr/bin/env python3
"""
Comprehensive Coastal Guardian Demo
Demonstrates all advanced features following the exact architecture specifications
"""

import pandas as pd
import json
import os
from datetime import datetime, timedelta
import numpy as np
from utils.auth import AuthManager
from utils.data_manager import DataManager
from utils.alerts import AlertEngine
from utils.ml_service import MLService

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"🌊 {title}")
    print(f"{'='*60}")

def demo_authentication():
    """Demonstrate authentication system"""
    print_header("AUTHENTICATION SYSTEM")
    
    auth = AuthManager()
    
    # Test login
    print("🔐 Testing Authentication:")
    user = auth.login("admin@coastalguardian.com", "demo123", "authority")
    if user:
        print(f"✅ Login successful: {user['name']} ({user['role']})")
    else:
        print("❌ Login failed")
    
    # Test user management
    print("\n👥 User Management:")
    users = auth.get_all_users()
    print(f"📊 Total users: {len(users)}")
    
    for user in users:
        print(f"  • {user['name']} - {user['role']} - {user['points']} pts")
    
    # Test API key generation
    print("\n🔑 API Key Management:")
    api_key = auth.generate_api_key(users[0]['_id'])
    print(f"✅ Generated API key: {api_key[:20]}...")
    
    # Test API key validation
    validated_user = auth.validate_api_key(api_key)
    if validated_user:
        print(f"✅ API key validated for: {validated_user['name']}")

def demo_data_management():
    """Demonstrate data management system"""
    print_header("DATA MANAGEMENT SYSTEM")
    
    data_manager = DataManager()
    
    # Test sensor data ingestion
    print("📊 Sensor Data Ingestion:")
    sensor_data = {
        "sourceId": "demo_sensor_001",
        "type": "tide",
        "value": 4.2,
        "unit": "m",
        "metadata": {"location": "Mumbai", "station": "Gateway"},
        "lat": 19.0760,
        "lng": 72.8777,
        "timestamp": datetime.now().isoformat()
    }
    
    reading = data_manager.save_sensor_reading(sensor_data)
    print(f"✅ Saved sensor reading: {reading['type']} = {reading['value']}{reading['unit']}")
    
    # Test report creation
    print("\n📝 Report Management:")
    report_data = {
        "userId": "demo_user_001",
        "type": "mangrove_cut",
        "description": "Large area of mangroves cleared for construction",
        "photoUrl": "reports/demo_mangrove_cut.jpg",
        "location": {"type": "Point", "coordinates": [72.8777, 19.0760]},
        "status": "pending",
        "score": 85
    }
    
    report = data_manager.save_report(report_data)
    print(f"✅ Created report: {report['type']} - {report['description'][:50]}...")
    
    # Test data retrieval
    print("\n📋 Data Retrieval:")
    reports = data_manager.get_all_reports()
    print(f"📊 Total reports: {len(reports)}")
    
    pending_reports = data_manager.get_pending_reports()
    print(f"⏳ Pending reports: {len(pending_reports)}")
    
    # Test system statistics
    stats = data_manager.get_system_stats()
    print(f"\n📈 System Statistics:")
    for key, value in stats.items():
        print(f"  • {key}: {value}")

def demo_alert_engine():
    """Demonstrate alert engine"""
    print_header("ALERT ENGINE")
    
    alert_engine = AlertEngine()
    
    # Load sample data
    print("📊 Loading Sample Data:")
    df = pd.read_csv("data/sample_sensor_data.csv")
    print(f"✅ Loaded {len(df)} sensor readings")
    
    # Process data for alerts
    print("\n🚨 Processing Alerts:")
    alerts = alert_engine.process_sensor_data(df)
    print(f"✅ Generated {len(alerts)} alerts")
    
    # Display alerts
    for i, alert in enumerate(alerts, 1):
        print(f"\n  Alert #{i}:")
        print(f"    Type: {alert['type']}")
        print(f"    Severity: {alert['severity']}")
        print(f"    Score: {alert['score']:.1f}")
        print(f"    Message: {alert['message']}")
    
    # Test anomaly detection
    print("\n🔍 Anomaly Detection:")
    tide_data = df[df['type'] == 'tide']['value'].tolist()
    anomalies = alert_engine.detect_anomalies(tide_data, 'tide')
    print(f"✅ Detected {len(anomalies)} anomalies")
    
    for anomaly in anomalies[:3]:  # Show first 3
        print(f"  • Index {anomaly['index']}: {anomaly['value']:.1f}m (z-score: {anomaly['z_score']:.1f})")
    
    # Test threat prediction
    print("\n🔮 Threat Prediction:")
    predictions = alert_engine.predict_threats(df)
    print(f"✅ Generated {len(predictions)} predictions")
    
    for pred in predictions:
        print(f"  • {pred['metric']}: trend={pred['trend']:.3f}, threat={pred['predicted_threat']}, confidence={pred['confidence']:.1f}%")
    
    # Test alert summary
    print("\n📊 Alert Summary:")
    summary = alert_engine.get_alert_summary(alerts)
    print(f"  • Total alerts: {summary['total_alerts']}")
    print(f"  • Average score: {summary['avg_score']:.1f}")
    print(f"  • By severity: {summary['by_severity']}")
    print(f"  • By type: {summary['by_type']}")

def demo_ml_service():
    """Demonstrate ML service"""
    print_header("MACHINE LEARNING SERVICE")
    
    ml_service = MLService()
    
    # Test image validation
    print("🖼️ Image Validation:")
    test_images = [
        "healthy_mangrove.jpg",
        "cut_mangrove.png", 
        "unknown_image.jpg"
    ]
    
    for img in test_images:
        confidence = ml_service.validate_image(img)
        health = ml_service.detect_mangrove_health(img)
        print(f"  • {img}: {health['status']} (confidence: {confidence:.1f}%)")
    
    # Test anomaly detection
    print("\n🔍 ML Anomaly Detection:")
    time_series = np.random.normal(100, 10, 50)  # Mock data
    time_series[25] = 150  # Add anomaly
    
    anomalies = ml_service.detect_anomalies(time_series, 'sea_level')
    print(f"✅ Detected {len(anomalies)} anomalies")
    
    for anomaly in anomalies[:3]:
        print(f"  • Index {anomaly['index']}: {anomaly['value']:.1f} (confidence: {anomaly['confidence']:.1f}%)")
    
    # Test sequence prediction
    print("\n🔮 Sequence Prediction:")
    historical_data = np.random.normal(2.5, 0.5, 30)  # Mock tide data
    predictions = ml_service.predict_sequence(historical_data, forecast_steps=6)
    print(f"✅ Generated {len(predictions)} predictions")
    
    for pred in predictions[:3]:
        print(f"  • Step {pred['step']}: {pred['predicted_value']:.2f}m (confidence: {pred['confidence']:.1f}%)")
    
    # Test report classification
    print("\n📝 Report Classification:")
    test_descriptions = [
        "Large area of mangroves cut down for construction",
        "Industrial waste being dumped into coastal waters",
        "Oil spill detected near the shoreline",
        "Unauthorized fishing activities observed"
    ]
    
    for desc in test_descriptions:
        classification = ml_service.classify_report_type(desc)
        print(f"  • '{desc[:30]}...': {classification['type']} (confidence: {classification['confidence']:.1f}%)")
    
    # Test feature extraction
    print("\n🔧 Feature Extraction:")
    features = ml_service.extract_features("demo_image.jpg")
    print("✅ Extracted features:")
    for key, value in features.items():
        if isinstance(value, list):
            print(f"  • {key}: {value}")
        else:
            print(f"  • {key}: {value:.3f}")
    
    # Test model info
    print("\n📊 Model Information:")
    model_info = ml_service.get_model_info()
    print(f"  • Total models: {model_info['total_models']}")
    print(f"  • Status: {model_info['status']}")
    for model_name, model_data in model_info['models'].items():
        print(f"  • {model_name}: v{model_data['version']} (accuracy: {model_data['accuracy']:.1%})")

def demo_integration():
    """Demonstrate system integration"""
    print_header("SYSTEM INTEGRATION")
    
    # Initialize all services
    auth = AuthManager()
    data_manager = DataManager()
    alert_engine = AlertEngine()
    ml_service = MLService()
    
    print("🔗 Testing End-to-End Workflow:")
    
    # 1. User submits report
    print("\n1️⃣ User Report Submission:")
    user = auth.login("community@coastalguardian.com", "demo123", "community")
    if user:
        report_data = {
            "userId": user['_id'],
            "type": "mangrove_cut",
            "description": "Mangrove clearing for new development project",
            "photoUrl": "reports/mangrove_clearing_2024.jpg",
            "location": {"type": "Point", "coordinates": [72.8777, 19.0760]},
            "status": "pending"
        }
        
        # ML validation
        confidence = ml_service.validate_image(report_data['photoUrl'])
        report_data['score'] = confidence
        
        report = data_manager.save_report(report_data)
        print(f"✅ Report submitted: {report['type']} (confidence: {confidence:.1f}%)")
    
    # 2. Authority verifies report
    print("\n2️⃣ Authority Verification:")
    authority = auth.login("admin@coastalguardian.com", "demo123", "authority")
    if authority:
        pending_reports = data_manager.get_pending_reports()
        if pending_reports:
            report = pending_reports[0]
            verified_report = data_manager.verify_report(report['_id'], 'verify')
            print(f"✅ Report verified: {verified_report['type']}")
            
            # Check updated user points
            updated_user = auth.get_user_by_id(user['_id'])
            print(f"📊 User points updated: {updated_user['points']}")
    
    # 3. Sensor data triggers alert
    print("\n3️⃣ Sensor Alert Generation:")
    sensor_data = {
        "sourceId": "sensor_001",
        "type": "tide",
        "value": 4.5,  # Above threshold
        "unit": "m",
        "metadata": {"location": "Mumbai"},
        "lat": 19.0760,
        "lng": 72.8777,
        "timestamp": datetime.now().isoformat()
    }
    
    # Save sensor reading
    reading = data_manager.save_sensor_reading(sensor_data)
    print(f"✅ Sensor reading saved: {reading['value']}{reading['unit']}")
    
    # Generate alert
    df = pd.DataFrame([sensor_data])
    alerts = alert_engine.process_sensor_data(df)
    
    if alerts:
        alert = alerts[0]
        saved_alert = data_manager.save_alert(alert)
        print(f"🚨 Alert generated: {alert['type']} (severity: {alert['severity']}, score: {alert['score']:.1f})")
        
        # Send notification
        data_manager.send_notification(alert)
        print("📱 Notification sent")
    
    # 4. Analytics and reporting
    print("\n4️⃣ Analytics & Reporting:")
    stats = data_manager.get_system_stats()
    print("📊 Current System Status:")
    for key, value in stats.items():
        print(f"  • {key}: {value}")
    
    # Leaderboard
    contributors = data_manager.get_top_contributors(limit=5)
    print(f"\n🏆 Top Contributors:")
    for i, contributor in enumerate(contributors, 1):
        print(f"  {i}. {contributor['name']} - {contributor['points']} pts ({contributor['role']})")

def demo_performance():
    """Demonstrate performance metrics"""
    print_header("PERFORMANCE METRICS")
    
    # Test data processing speed
    print("⚡ Performance Testing:")
    
    # Generate large dataset
    print("📊 Generating test dataset...")
    large_df = pd.DataFrame({
        'timestamp': pd.date_range(start='2024-01-01', periods=1000, freq='H'),
        'tide_level': np.random.normal(2.5, 0.8, 1000),
        'sea_level': np.random.normal(1.0, 0.3, 1000),
        'wave_height': np.random.normal(1.5, 0.5, 1000),
        'wind_speed': np.random.normal(15.0, 5.0, 1000)
    })
    
    print(f"✅ Generated {len(large_df)} records")
    
    # Test alert processing speed
    import time
    start_time = time.time()
    
    alert_engine = AlertEngine()
    alerts = alert_engine.process_sensor_data(large_df)
    
    processing_time = time.time() - start_time
    print(f"🚨 Alert processing: {len(alerts)} alerts in {processing_time:.3f}s")
    print(f"📈 Processing rate: {len(large_df)/processing_time:.0f} records/second")
    
    # Test ML inference speed
    print("\n🤖 ML Inference Testing:")
    ml_service = MLService()
    
    start_time = time.time()
    for i in range(100):
        confidence = ml_service.validate_image(f"test_image_{i}.jpg")
    
    inference_time = time.time() - start_time
    print(f"🖼️ Image validation: 100 images in {inference_time:.3f}s")
    print(f"📈 Inference rate: {100/inference_time:.0f} images/second")

def main():
    """Run comprehensive demo"""
    print("🌊 COASTAL GUARDIAN - COMPREHENSIVE DEMO")
    print("=" * 60)
    print(f"🕐 Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📋 Following exact architecture specifications")
    
    try:
        # Run all demos
        demo_authentication()
        demo_data_management()
        demo_alert_engine()
        demo_ml_service()
        demo_integration()
        demo_performance()
        
        print_header("DEMO COMPLETED SUCCESSFULLY")
        print("🎉 All systems operational!")
        print("🌊 Coastal Guardian is ready for production deployment!")
        print("\n📊 Key Features Demonstrated:")
        print("  ✅ Role-based authentication system")
        print("  ✅ GeoJSON-compliant data models")
        print("  ✅ Unified alert scoring (0-100)")
        print("  ✅ ML-powered image validation")
        print("  ✅ Real-time anomaly detection")
        print("  ✅ Gamified community engagement")
        print("  ✅ Comprehensive analytics")
        print("  ✅ High-performance processing")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
