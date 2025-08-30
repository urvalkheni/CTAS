import pandas as pd
import sqlite3
from datetime import datetime
from utils.data_collector import DataCollector
from sklearn.ensemble import IsolationForest

class AlertSystem:
    def __init__(self):
        self.data_collector = DataCollector()
        
    def detect_and_alert(self):
        """Main function to detect threats and generate alerts"""
        # Load data from database
        conn = sqlite3.connect('coastal_data.db')
        df = pd.read_sql_query("SELECT * FROM coastal_data", conn)
        conn.close()
        
        if df.empty:
            print("No data available for threat detection.")
            return
            
        print("Running threat detection...")
        
        # Detect anomalies for each parameter
        for param in df['parameter'].unique():
            anomalies = self._detect_anomalies(df, param)
            
            if not anomalies.empty:
                # Generate alerts for detected anomalies
                for _, anomaly in anomalies.iterrows():
                    self._generate_alert(anomaly, param)
                    
        print("Threat detection and alerting completed.")
    
    def _detect_anomalies(self, df, parameter):
        """Detect anomalies for a specific parameter"""
        param_df = df[df['parameter'] == parameter]
        
        if param_df.empty or len(param_df) < 5:  # Need minimum data points
            return pd.DataFrame()
            
        X = param_df[['value']].values
        model = IsolationForest(contamination=0.1, random_state=42)
        param_df = param_df.copy()
        param_df['anomaly'] = model.fit_predict(X)
        
        anomalies = param_df[param_df['anomaly'] == -1]
        return anomalies
    
    def _generate_alert(self, anomaly_row, parameter):
        """Generate and save alert for detected anomaly"""
        # Determine severity based on parameter and value
        severity = self._calculate_severity(parameter, anomaly_row['value'])
        
        # Create alert message
        message = self._create_alert_message(parameter, anomaly_row['value'], severity)
        
        # Save alert to database
        alert_data = {
            'type': f'{parameter}_anomaly',
            'severity': severity,
            'score': self._calculate_threat_score(parameter, anomaly_row['value']),
            'message': message,
            'location': {'type': 'Point', 'coordinates': [72.8777, 19.0760]},  # Default location
            'evidence': [anomaly_row['id']]
        }
        
        saved_alert = self.data_collector.save_alert(alert_data)
        print(f"🚨 Alert generated: {message}")
        
        # Send notifications
        self._send_notifications(saved_alert)
        
        return saved_alert
    
    def _calculate_severity(self, parameter, value):
        """Calculate alert severity based on parameter and value"""
        # Define thresholds for different parameters
        thresholds = {
            'tide_level': {'critical': 4.0, 'high': 3.5, 'moderate': 3.0},
            'wind_speed': {'critical': 50.0, 'high': 40.0, 'moderate': 30.0},
            'pollution_index': {'critical': 80.0, 'high': 60.0, 'moderate': 40.0},
            'sea_temp': {'critical': 35.0, 'high': 32.0, 'moderate': 30.0}
        }
        
        if parameter in thresholds:
            thresh = thresholds[parameter]
            if value >= thresh['critical']:
                return 'critical'
            elif value >= thresh['high']:
                return 'high'
            elif value >= thresh['moderate']:
                return 'moderate'
        
        return 'low'
    
    def _calculate_threat_score(self, parameter, value):
        """Calculate numerical threat score (0-100)"""
        # Simple scoring based on value ranges
        if parameter == 'tide_level':
            return min(100, (value / 4.0) * 100)
        elif parameter == 'wind_speed':
            return min(100, (value / 60.0) * 100)
        elif parameter == 'pollution_index':
            return min(100, value)
        elif parameter == 'sea_temp':
            return min(100, ((value - 20) / 15) * 100)
        
        return 50  # Default score
    
    def _create_alert_message(self, parameter, value, severity):
        """Create human-readable alert message"""
        param_names = {
            'tide_level': 'Tide Level',
            'wind_speed': 'Wind Speed',
            'pollution_index': 'Pollution Index',
            'sea_temp': 'Sea Surface Temperature',
            'cyclone_alert': 'Cyclone Activity'
        }
        
        param_name = param_names.get(parameter, parameter.replace('_', ' ').title())
        
        return f"{severity.upper()}: Abnormal {param_name} detected - Value: {value}"
    
    def _send_notifications(self, alert):
        """Send notifications for the alert"""
        # Mock notification system - in production, integrate with actual services
        print(f"📱 SMS Notification: {alert['message']}")
        print(f"📧 Email Notification: Alert sent to authorities")
        print(f"🔔 Push Notification: {alert['type']} - {alert['severity']}")
        
        # Update notification status in database
        self.data_collector.send_notification(alert)

if __name__ == '__main__':
    alert_system = AlertSystem()
    alert_system.detect_and_alert()
