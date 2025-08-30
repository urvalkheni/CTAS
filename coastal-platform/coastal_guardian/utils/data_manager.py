import json
import os
import uuid
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class DataManager:
    def __init__(self):
        self.data_dir = "data"
        self.reports_dir = "reports"
        self._ensure_directories()
        self._init_data_files()
    
    def _ensure_directories(self):
        """Ensure data directories exist"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def _init_data_files(self):
        """Initialize data files if they don't exist"""
        files_to_init = {
            "sensor_readings.json": {"readings": []},
            "reports.json": {"reports": []},
            "alerts.json": {"alerts": []},
            "gamification_logs.json": {"logs": []}
        }
        
        for filename, default_data in files_to_init.items():
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w') as f:
                    json.dump(default_data, f, indent=2)
    
    def _load_data(self, filename):
        """Load data from JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _save_data(self, filename, data):
        """Save data to JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    # Sensor Readings
    def save_sensor_reading(self, reading_data):
        """Save sensor reading following SensorReading schema"""
        data = self._load_data("sensor_readings.json")
        
        reading = {
            "_id": str(uuid.uuid4()),
            "sourceId": reading_data.get("sourceId", "unknown"),
            "type": reading_data.get("type", "unknown"),
            "value": reading_data.get("value", 0),
            "unit": reading_data.get("unit", ""),
            "metadata": reading_data.get("metadata", {}),
            "location": {
                "type": "Point",
                "coordinates": [reading_data.get("lng", 0), reading_data.get("lat", 0)]
            },
            "timestamp": reading_data.get("timestamp", datetime.now().isoformat()),
            "readingId": reading_data.get("readingId", str(uuid.uuid4()))
        }
        
        data["readings"].append(reading)
        self._save_data("sensor_readings.json", data)
        return reading
    
    def get_sensor_readings(self, sensor_type=None, start_date=None, end_date=None):
        """Get sensor readings with optional filters"""
        data = self._load_data("sensor_readings.json")
        readings = data.get("readings", [])
        
        if sensor_type:
            readings = [r for r in readings if r["type"] == sensor_type]
        
        if start_date:
            readings = [r for r in readings if datetime.fromisoformat(r["timestamp"]) >= start_date]
        
        if end_date:
            readings = [r for r in readings if datetime.fromisoformat(r["timestamp"]) <= end_date]
        
        return readings
    
    # Reports
    def save_report(self, report_data):
        """Save report following Report schema"""
        data = self._load_data("reports.json")
        
        report = {
            "_id": str(uuid.uuid4()),
            "userId": report_data.get("userId"),
            "type": report_data.get("type"),
            "description": report_data.get("description", ""),
            "photoUrl": report_data.get("photoUrl", ""),
            "location": report_data.get("location"),
            "status": report_data.get("status", "pending"),
            "verifierId": report_data.get("verifierId"),
            "score": report_data.get("score", 0),
            "createdAt": report_data.get("createdAt", datetime.now().isoformat()),
            "updatedAt": datetime.now().isoformat()
        }
        
        data["reports"].append(report)
        self._save_data("reports.json", data)
        return report
    
    def get_all_reports(self):
        """Get all reports"""
        data = self._load_data("reports.json")
        return data.get("reports", [])
    
    def get_pending_reports(self):
        """Get pending reports"""
        reports = self.get_all_reports()
        return [r for r in reports if r["status"] == "pending"]
    
    def verify_report(self, report_id, action):
        """Verify or reject a report"""
        data = self._load_data("reports.json")
        
        for i, report in enumerate(data["reports"]):
            if report["_id"] == report_id:
                data["reports"][i]["status"] = action
                data["reports"][i]["updatedAt"] = datetime.now().isoformat()
                
                # Add points if verified
                if action == "verify":
                    self._add_gamification_log(
                        report["userId"],
                        "report_verified",
                        10,
                        report_id
                    )
                
                self._save_data("reports.json", data)
                return data["reports"][i]
        
        return None
    
    # Alerts
    def save_alert(self, alert_data):
        """Save alert following Alert schema"""
        data = self._load_data("alerts.json")
        
        alert = {
            "_id": str(uuid.uuid4()),
            "evidence": alert_data.get("evidence", []),
            "type": alert_data.get("type"),
            "severity": alert_data.get("severity", "low"),
            "score": alert_data.get("score", 0),
            "location": alert_data.get("location"),
            "message": alert_data.get("message", ""),
            "createdAt": alert_data.get("createdAt", datetime.now().isoformat()),
            "notified": {
                "smsSent": False,
                "emailSent": False,
                "pushSent": False
            }
        }
        
        data["alerts"].append(alert)
        self._save_data("alerts.json", data)
        return alert
    
    def get_all_alerts(self):
        """Get all alerts"""
        data = self._load_data("alerts.json")
        return data.get("alerts", [])
    
    def get_active_alerts(self):
        """Get active alerts (not acknowledged)"""
        alerts = self.get_all_alerts()
        # For demo, consider all alerts as active
        return alerts
    
    def get_alerts_in_range(self, start_date, end_date):
        """Get alerts within date range"""
        alerts = self.get_all_alerts()
        filtered_alerts = []
        
        for alert in alerts:
            alert_date = datetime.fromisoformat(alert["createdAt"]).date()
            if start_date <= alert_date <= end_date:
                filtered_alerts.append(alert)
        
        return filtered_alerts
    
    def acknowledge_alert(self, alert_id):
        """Acknowledge an alert"""
        data = self._load_data("alerts.json")
        
        for i, alert in enumerate(data["alerts"]):
            if alert["_id"] == alert_id:
                data["alerts"][i]["acknowledged"] = True
                data["alerts"][i]["acknowledgedAt"] = datetime.now().isoformat()
                self._save_data("alerts.json", data)
                return data["alerts"][i]
        
        return None
    
    def send_notification(self, alert):
        """Send notification for alert"""
        # Mock notification - in production this would integrate with Twilio/SendGrid
        print(f"📱 Mock SMS sent for alert: {alert['type']}")
        print(f"📧 Mock email sent for alert: {alert['type']}")
        
        # Update notification status
        data = self._load_data("alerts.json")
        for i, a in enumerate(data["alerts"]):
            if a["_id"] == alert["_id"]:
                data["alerts"][i]["notified"]["smsSent"] = True
                data["alerts"][i]["notified"]["emailSent"] = True
                self._save_data("alerts.json", data)
                break
    
    # Gamification
    def _add_gamification_log(self, user_id, action, points, related_id=None):
        """Add gamification log entry"""
        data = self._load_data("gamification_logs.json")
        
        log_entry = {
            "_id": str(uuid.uuid4()),
            "userId": user_id,
            "action": action,
            "points": points,
            "relatedId": related_id,
            "createdAt": datetime.now().isoformat()
        }
        
        data["logs"].append(log_entry)
        self._save_data("gamification_logs.json", data)
        
        # Update user points
        from .auth import AuthManager
        auth = AuthManager()
        auth.add_points(user_id, points)
    
    def get_top_contributors(self, limit=10):
        """Get top contributors by points"""
        from .auth import AuthManager
        auth = AuthManager()
        users = auth.get_all_users()
        
        # Sort by points descending
        sorted_users = sorted(users, key=lambda x: x.get('points', 0), reverse=True)
        return sorted_users[:limit]
    
    # Map data
    def get_map_data(self):
        """Get data for map visualization"""
        alerts = self.get_active_alerts()
        reports = self.get_pending_reports()
        
        return {
            "alerts": alerts,
            "reports": reports
        }
    
    # Trends and analytics
    def get_trend_data(self, metrics, start_date, end_date):
        """Get trend data for specified metrics"""
        # For demo, generate sample trend data
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        trend_data = {
            'timestamp': dates,
            'sea_level': np.random.normal(1.0, 0.3, len(dates)),
            'tide_level': np.random.normal(2.5, 0.8, len(dates)),
            'wave_height': np.random.normal(1.5, 0.5, len(dates)),
            'wind_speed': np.random.normal(15.0, 5.0, len(dates)),
            'turbidity': np.random.normal(5.0, 2.0, len(dates))
        }
        
        df = pd.DataFrame(trend_data)
        
        # Filter to requested metrics
        if metrics:
            available_metrics = ['timestamp'] + [m for m in metrics if m in df.columns]
            df = df[available_metrics]
        
        return df
    
    # User management
    def get_all_users(self):
        """Get all users"""
        from .auth import AuthManager
        auth = AuthManager()
        return auth.get_all_users()
    
    # Statistics
    def get_system_stats(self):
        """Get system statistics"""
        return {
            "total_users": len(self.get_all_users()),
            "total_reports": len(self.get_all_reports()),
            "pending_reports": len(self.get_pending_reports()),
            "active_alerts": len(self.get_active_alerts()),
            "total_sensor_readings": len(self.get_sensor_readings())
        }
