#!/usr/bin/env python3
"""
Coastal Guardian Alert & Notification System Demo
Demonstrates the enhanced alert system with SMS/email notifications
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Add the utils directory to the path
sys.path.append('utils')

from alerts import AlertEngine

def create_test_sensor_data():
    """Create test sensor data with anomalies to trigger alerts"""
    print("📊 Creating test sensor data...")
    
    # Generate 24 hours of data
    timestamps = pd.date_range(start=datetime.now() - timedelta(hours=24), 
                              end=datetime.now(), freq='H')
    
    # Normal baseline values
    base_tide = 2.0
    base_sea_level = 0.8
    base_wave_height = 1.2
    base_wind_speed = 15.0
    base_turbidity = 5.0
    
    # Create data with some anomalies
    data = []
    for i, timestamp in enumerate(timestamps):
        # Add some random variation
        tide_level = base_tide + np.random.normal(0, 0.3)
        sea_level = base_sea_level + np.random.normal(0, 0.2)
        wave_height = base_wave_height + np.random.normal(0, 0.4)
        wind_speed = base_wind_speed + np.random.normal(0, 5.0)
        turbidity = base_turbidity + np.random.normal(0, 2.0)
        
        # Add anomalies at specific times
        if i == 18:  # High tide alert
            tide_level = 4.2  # Above 3.5 threshold
        elif i == 20:  # High wind alert
            wind_speed = 35.0  # Above 25.0 threshold
        elif i == 22:  # High wave alert
            wave_height = 3.8  # Above 2.5 threshold
        
        data.append({
            'timestamp': timestamp,
            'tide_level': round(tide_level, 2),
            'sea_level': round(sea_level, 2),
            'wave_height': round(wave_height, 2),
            'wind_speed': round(wind_speed, 2),
            'turbidity': round(turbidity, 2)
        })
    
    df = pd.DataFrame(data)
    print(f"✅ Created {len(df)} sensor data records")
    return df

def demo_alert_engine():
    """Demonstrate the alert engine functionality"""
    print("\n🚨 ALERT ENGINE DEMONSTRATION")
    print("=" * 50)
    
    # Initialize alert engine
    alert_engine = AlertEngine()
    
    # Create test data
    sensor_data = create_test_sensor_data()
    
    # Process sensor data to generate alerts
    print("\n🔍 Processing sensor data for alerts...")
    alerts = alert_engine.process_sensor_data(sensor_data)
    
    if alerts:
        print(f"\n🚨 Generated {len(alerts)} alerts:")
        for i, alert in enumerate(alerts, 1):
            print(f"\n  {i}. {alert['type'].upper()} Alert")
            print(f"     Severity: {alert['severity'].upper()}")
            print(f"     Message: {alert['message']}")
            print(f"     Score: {alert['score']:.1f}/100")
            print(f"     Time: {alert['createdAt']}")
    else:
        print("✅ No alerts generated")
    
    return alerts

def demo_alert_management():
    """Demonstrate alert management features"""
    print("\n📋 ALERT MANAGEMENT DEMONSTRATION")
    print("=" * 50)
    
    alert_engine = AlertEngine()
    
    # Get active alerts
    active_alerts = alert_engine.get_active_alerts()
    print(f"📊 Active alerts: {len(active_alerts)}")
    
    if active_alerts:
        # Show alert summary
        summary = alert_engine.get_alert_summary(active_alerts)
        print(f"\n📈 Alert Summary:")
        print(f"   Total: {summary['total_alerts']}")
        print(f"   By Severity: {summary['by_severity']}")
        print(f"   By Type: {summary['by_type']}")
        print(f"   Average Score: {summary['avg_score']:.1f}")
        
        # Demonstrate acknowledging an alert
        if active_alerts:
            first_alert = active_alerts[0]
            print(f"\n✅ Acknowledging alert: {first_alert['id']}")
            success = alert_engine.acknowledge_alert(first_alert['id'], 'demo_user')
            if success:
                print("   Alert acknowledged successfully")
            else:
                print("   Failed to acknowledge alert")
    
    return active_alerts

def demo_anomaly_detection():
    """Demonstrate anomaly detection capabilities"""
    print("\n🔍 ANOMALY DETECTION DEMONSTRATION")
    print("=" * 50)
    
    alert_engine = AlertEngine()
    
    # Create test data with anomalies
    sensor_data = create_test_sensor_data()
    
    # Detect anomalies in different metrics
    metrics = ['tide_level', 'sea_level', 'wave_height', 'wind_speed', 'turbidity']
    
    for metric in metrics:
        anomalies = alert_engine.detect_anomalies(sensor_data, metric)
        if anomalies:
            print(f"\n📊 {metric.replace('_', ' ').title()} Anomalies:")
            for anomaly in anomalies[:3]:  # Show first 3
                print(f"   Value: {anomaly['value']:.2f}, Z-score: {anomaly['z_score']:.2f}")
        else:
            print(f"✅ No anomalies detected in {metric}")

def demo_threat_prediction():
    """Demonstrate threat prediction capabilities"""
    print("\n🔮 THREAT PREDICTION DEMONSTRATION")
    print("=" * 50)
    
    alert_engine = AlertEngine()
    
    # Create historical data
    sensor_data = create_test_sensor_data()
    
    # Predict threats
    predictions = alert_engine.predict_threats(sensor_data, forecast_hours=24)
    
    if predictions:
        print(f"\n🔮 Threat Predictions:")
        for prediction in predictions:
            trend_direction = "increasing" if prediction['trend'] > 0 else "decreasing"
            print(f"   {prediction['metric']}: {trend_direction} trend")
            print(f"     Confidence: {prediction['confidence']:.1f}%")
            print(f"     Threat: {'Yes' if prediction['predicted_threat'] else 'No'}")
    else:
        print("✅ No significant threats predicted")

def demo_notification_config():
    """Demonstrate notification configuration"""
    print("\n📱 NOTIFICATION CONFIGURATION")
    print("=" * 50)
    
    alert_engine = AlertEngine()
    
    print("Current notification settings:")
    for key, value in alert_engine.notification_config.items():
        print(f"   {key}: {value}")
    
    print(f"\nTwilio available: {hasattr(alert_engine, 'twilio_client') and alert_engine.twilio_client is not None}")
    print(f"SMTP available: {SMTP_AVAILABLE if 'SMTP_AVAILABLE' in globals() else 'Unknown'}")
    
    # Show configuration
    print(f"\nConfiguration loaded:")
    print(f"   SMS recipients: {alert_engine.config['recipients']['sms']}")
    print(f"   Email recipients: {alert_engine.config['recipients']['email']}")

def main():
    """Main demonstration function"""
    print("🌊 COASTAL GUARDIAN - ALERT & NOTIFICATION SYSTEM DEMO")
    print("=" * 60)
    print(f"🕐 Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Run all demonstrations
        alerts = demo_alert_engine()
        demo_alert_management()
        demo_anomaly_detection()
        demo_threat_prediction()
        demo_notification_config()
        
        print("\n" + "=" * 60)
        print("🎉 ALERT SYSTEM DEMO COMPLETED SUCCESSFULLY!")
        print("✅ All features demonstrated:")
        print("   • Alert generation from sensor data")
        print("   • SMS/Email notifications (if configured)")
        print("   • Console and file logging")
        print("   • Alert persistence to alerts.json")
        print("   • Anomaly detection")
        print("   • Threat prediction")
        print("   • Alert management (acknowledge/resolve)")
        
        if alerts:
            print(f"\n🚨 Generated {len(alerts)} test alerts")
            print("   Check logs/alerts.log for detailed logging")
            print("   Check data/alerts.json for stored alerts")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
