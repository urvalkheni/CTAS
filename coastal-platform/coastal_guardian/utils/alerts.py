import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid
import json
import os
import logging
from typing import Dict, List, Optional, Union

# Try to import Twilio for SMS notifications
try:
    from twilio.rest import Client
    from twilio.base.exceptions import TwilioException
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    print("⚠️ Twilio not available. SMS notifications disabled.")

# Try to import smtplib for email notifications
try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    SMTP_AVAILABLE = True
except ImportError:
    SMTP_AVAILABLE = False
    print("⚠️ smtplib not available. Email notifications disabled.")

class AlertEngine:
    def __init__(self, config_file: str = "data/api_keys.json"):
        # Default thresholds
        self.thresholds = {
            'tide': 3.5,
            'sea_level': 1.5,
            'wave': 2.5,
            'wind': 25.0,
            'turbidity': 10.0
        }
        
        # Alert scoring weights
        self.weights = {
            'tide': 0.3,
            'wind': 0.2,
            'trend': 0.2,
            'reports': 0.15,
            'ml': 0.15
        }
        
        # Notification settings
        self.notification_config = {
            'sms_enabled': True,
            'email_enabled': True,
            'console_logging': True,
            'file_logging': True,
            'min_severity_for_sms': 'high',
            'min_severity_for_email': 'moderate'
        }
        
        # Load configuration
        self.config = self._load_config(config_file)
        
        # Setup logging
        self._setup_logging()
        
        # Initialize notification clients
        self._init_notification_clients()
    
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from file"""
        # Default configuration
        default_config = {
            'twilio': {
                'account_sid': os.getenv('TWILIO_ACCOUNT_SID', ''),
                'auth_token': os.getenv('TWILIO_AUTH_TOKEN', ''),
                'from_number': os.getenv('TWILIO_FROM_NUMBER', '')
            },
            'email': {
                'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
                'smtp_port': int(os.getenv('SMTP_PORT', '587')),
                'username': os.getenv('EMAIL_USERNAME', ''),
                'password': os.getenv('EMAIL_PASSWORD', ''),
                'from_email': os.getenv('FROM_EMAIL', '')
            },
            'recipients': {
                'sms': os.getenv('SMS_RECIPIENTS', '+1234567890').split(','),
                'email': os.getenv('EMAIL_RECIPIENTS', 'admin@coastalguardian.com').split(',')
            }
        }
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    file_config = json.load(f)
                    # Merge file config with default config
                    if 'twilio' in file_config:
                        default_config['twilio'].update(file_config['twilio'])
                    if 'email' in file_config:
                        default_config['email'].update(file_config['email'])
                    if 'recipients' in file_config:
                        default_config['recipients'].update(file_config['recipients'])
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
        
        return default_config
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        if self.notification_config['console_logging']:
            logging.basicConfig(level=logging.INFO, format=log_format)
        
        if self.notification_config['file_logging']:
            # Create logs directory if it doesn't exist
            os.makedirs('logs', exist_ok=True)
            
            # File handler for alerts
            alert_handler = logging.FileHandler('logs/alerts.log')
            alert_handler.setLevel(logging.INFO)
            alert_handler.setFormatter(logging.Formatter(log_format))
            
            # Get logger and add handler
            self.logger = logging.getLogger('CoastalGuardian.Alerts')
            self.logger.addHandler(alert_handler)
            self.logger.setLevel(logging.INFO)
    
    def _init_notification_clients(self):
        """Initialize notification clients"""
        # Initialize Twilio client
        if TWILIO_AVAILABLE and self.config['twilio']['account_sid']:
            try:
                self.twilio_client = Client(
                    self.config['twilio']['account_sid'],
                    self.config['twilio']['auth_token']
                )
                logging.info("✅ Twilio client initialized successfully")
            except Exception as e:
                logging.error(f"❌ Failed to initialize Twilio client: {e}")
                self.twilio_client = None
        else:
            self.twilio_client = None
            logging.warning("⚠️ Twilio not configured or not available")
        
        # Email client will be initialized when needed
    
    def update_thresholds(self, new_thresholds: Dict):
        """Update alert thresholds"""
        self.thresholds.update(new_thresholds)
        logging.info(f"Updated thresholds: {new_thresholds}")
    
    def process_sensor_data(self, df: pd.DataFrame) -> List[Dict]:
        """Process sensor data and generate alerts"""
        alerts = []
        
        if df is None or df.empty:
            logging.warning("No sensor data provided for processing")
            return alerts
        
        # Ensure timestamp column exists
        if 'timestamp' not in df.columns:
            df['timestamp'] = pd.date_range(start=datetime.now(), periods=len(df), freq='H')
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Process each row for alerts
        for idx, row in df.iterrows():
            alert = self._analyze_row(row, df)
            if alert:
                alerts.append(alert)
                # Send notifications for this alert
                self._send_notifications(alert)
        
        # Save alerts to file
        if alerts:
            self._save_alerts(alerts)
            logging.info(f"Generated {len(alerts)} new alerts")
        
        return alerts
    
    def _analyze_row(self, row: pd.Series, df: pd.DataFrame) -> Optional[Dict]:
        """Analyze a single row for potential alerts"""
        alert = None
        
        # Check tide level
        if 'tide_level' in row and row['tide_level'] > self.thresholds['tide']:
            alert = self._create_alert(
                type="storm_surge",
                severity=self._calculate_severity(row['tide_level'], self.thresholds['tide']),
                message=f"🚨 High tide detected: {row['tide_level']:.1f}m (threshold: {self.thresholds['tide']}m)",
                location={'type': 'Point', 'coordinates': [72.8777, 19.0760]},  # Mumbai
                score=self._calculate_score(row, df, 'tide_level'),
                metric='tide_level',
                value=row['tide_level']
            )
        
        # Check sea level
        elif 'sea_level' in row and row['sea_level'] > self.thresholds['sea_level']:
            alert = self._create_alert(
                type="sea_level_rise",
                severity=self._calculate_severity(row['sea_level'], self.thresholds['sea_level']),
                message=f"⚠️ Elevated sea level: {row['sea_level']:.1f}m (threshold: {self.thresholds['sea_level']}m)",
                location={'type': 'Point', 'coordinates': [72.8777, 19.0760]},
                score=self._calculate_score(row, df, 'sea_level'),
                metric='sea_level',
                value=row['sea_level']
            )
        
        # Check wave height
        elif 'wave_height' in row and row['wave_height'] > self.thresholds['wave']:
            alert = self._create_alert(
                type="high_waves",
                severity=self._calculate_severity(row['wave_height'], self.thresholds['wave']),
                message=f"🌊 High waves detected: {row['wave_height']:.1f}m (threshold: {self.thresholds['wave']}m)",
                location={'type': 'Point', 'coordinates': [72.8777, 19.0760]},
                score=self._calculate_score(row, df, 'wave_height'),
                metric='wave_height',
                value=row['wave_height']
            )
        
        # Check wind speed
        elif 'wind_speed' in row and row['wind_speed'] > self.thresholds['wind']:
            alert = self._create_alert(
                type="high_winds",
                severity=self._calculate_severity(row['wind_speed'], self.thresholds['wind']),
                message=f"💨 High wind speed: {row['wind_speed']:.1f} km/h (threshold: {self.thresholds['wind']} km/h)",
                location={'type': 'Point', 'coordinates': [72.8777, 19.0760]},
                score=self._calculate_score(row, df, 'wind_speed'),
                metric='wind_speed',
                value=row['wind_speed']
            )
        
        # Check turbidity
        elif 'turbidity' in row and row['turbidity'] > self.thresholds['turbidity']:
            alert = self._create_alert(
                type="water_pollution",
                severity=self._calculate_severity(row['turbidity'], self.thresholds['turbidity']),
                message=f"🌊 High turbidity detected: {row['turbidity']:.1f} NTU (threshold: {self.thresholds['turbidity']} NTU)",
                location={'type': 'Point', 'coordinates': [72.8777, 19.0760]},
                score=self._calculate_score(row, df, 'turbidity'),
                metric='turbidity',
                value=row['turbidity']
            )
        
        return alert
    
    def _create_alert(self, type: str, severity: str, message: str, location: Dict, score: float, metric: str = None, value: float = None) -> Dict:
        """Create alert object"""
        alert = {
            'id': str(uuid.uuid4()),
            'type': type,
            'severity': severity,
            'message': message,
            'location': location,
            'score': score,
            'createdAt': datetime.now().isoformat(),
            'evidence': [],
            'status': 'active',
            'acknowledged': False,
            'acknowledged_by': None,
            'acknowledged_at': None
        }
        
        if metric:
            alert['metric'] = metric
        if value:
            alert['value'] = value
        
        return alert
    
    def _send_notifications(self, alert: Dict):
        """Send notifications for an alert based on severity"""
        severity = alert['severity']
        
        # Console logging
        if self.notification_config['console_logging']:
            self._log_alert(alert)
        
        # SMS notifications for high/critical alerts
        if (self.notification_config['sms_enabled'] and 
            self.twilio_client and 
            self._should_send_sms(severity)):
            self._send_sms_alert(alert)
        
        # Email notifications for moderate+ alerts
        if (self.notification_config['email_enabled'] and 
            self._should_send_email(severity)):
            self._send_email_alert(alert)
    
    def _should_send_sms(self, severity: str) -> bool:
        """Check if SMS should be sent for this severity"""
        severity_levels = {'low': 1, 'moderate': 2, 'high': 3, 'critical': 4}
        min_level = severity_levels.get(self.notification_config['min_severity_for_sms'], 3)
        return severity_levels.get(severity, 1) >= min_level
    
    def _should_send_email(self, severity: str) -> bool:
        """Check if email should be sent for this severity"""
        severity_levels = {'low': 1, 'moderate': 2, 'high': 3, 'critical': 4}
        min_level = severity_levels.get(self.notification_config['min_severity_for_email'], 2)
        return severity_levels.get(severity, 1) >= min_level
    
    def _log_alert(self, alert: Dict):
        """Log alert to console and file"""
        log_message = f"🚨 ALERT: {alert['type'].upper()} - {alert['severity'].upper()} - {alert['message']}"
        
        if alert['severity'] == 'critical':
            logging.critical(log_message)
        elif alert['severity'] == 'high':
            logging.error(log_message)
        elif alert['severity'] == 'moderate':
            logging.warning(log_message)
        else:
            logging.info(log_message)
        
        # Also log to file if configured
        if hasattr(self, 'logger'):
            self.logger.info(log_message)
    
    def _send_sms_alert(self, alert: Dict):
        """Send SMS alert using Twilio"""
        if not self.twilio_client:
            return
        
        try:
            message_body = f"🚨 COASTAL ALERT: {alert['type'].upper()}\n{alert['message']}\nSeverity: {alert['severity'].upper()}\nScore: {alert['score']:.1f}/100"
            
            for phone_number in self.config['recipients']['sms']:
                if phone_number.strip():
                    message = self.twilio_client.messages.create(
                        body=message_body,
                        from_=self.config['twilio']['from_number'],
                        to=phone_number.strip()
                    )
                    logging.info(f"✅ SMS sent to {phone_number}: {message.sid}")
        
        except TwilioException as e:
            logging.error(f"❌ Failed to send SMS: {e}")
        except Exception as e:
            logging.error(f"❌ Unexpected error sending SMS: {e}")
    
    def _send_email_alert(self, alert: Dict):
        """Send email alert using SMTP"""
        if not SMTP_AVAILABLE:
            return
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.config['email']['from_email']
            msg['To'] = ', '.join(self.config['recipients']['email'])
            msg['Subject'] = f"🚨 COASTAL ALERT: {alert['type'].upper()} - {alert['severity'].upper()}"
            
            # Create HTML body
            html_body = f"""
            <html>
            <body>
                <h2 style="color: {'#d32f2f' if alert['severity'] in ['high', 'critical'] else '#f57c00'};">
                    🚨 COASTAL ALERT
                </h2>
                <p><strong>Type:</strong> {alert['type'].upper()}</p>
                <p><strong>Severity:</strong> {alert['severity'].upper()}</p>
                <p><strong>Message:</strong> {alert['message']}</p>
                <p><strong>Alert Score:</strong> {alert['score']:.1f}/100</p>
                <p><strong>Location:</strong> {alert['location']['coordinates']}</p>
                <p><strong>Time:</strong> {alert['createdAt']}</p>
                <hr>
                <p><em>This is an automated alert from Coastal Guardian System</em></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.config['email']['smtp_server'], self.config['email']['smtp_port'])
            server.starttls()
            server.login(self.config['email']['username'], self.config['email']['password'])
            
            text = msg.as_string()
            server.sendmail(self.config['email']['from_email'], self.config['recipients']['email'], text)
            server.quit()
            
            logging.info(f"✅ Email alert sent to {', '.join(self.config['recipients']['email'])}")
        
        except Exception as e:
            logging.error(f"❌ Failed to send email alert: {e}")
    
    def _save_alerts(self, new_alerts: List[Dict]):
        """Save alerts to alerts.json file"""
        try:
            alerts_file = 'data/alerts.json'
            
            # Load existing alerts
            existing_alerts = []
            if os.path.exists(alerts_file):
                with open(alerts_file, 'r') as f:
                    data = json.load(f)
                    existing_alerts = data.get('alerts', [])
            
            # Add new alerts
            existing_alerts.extend(new_alerts)
            
            # Keep only last 1000 alerts to prevent file from growing too large
            if len(existing_alerts) > 1000:
                existing_alerts = existing_alerts[-1000:]
            
            # Save back to file
            with open(alerts_file, 'w') as f:
                json.dump({'alerts': existing_alerts}, f, indent=2)
            
            logging.info(f"✅ Saved {len(new_alerts)} new alerts to {alerts_file}")
        
        except Exception as e:
            logging.error(f"❌ Failed to save alerts: {e}")
    
    def get_active_alerts(self) -> List[Dict]:
        """Get all active alerts from alerts.json"""
        try:
            alerts_file = 'data/alerts.json'
            if os.path.exists(alerts_file):
                with open(alerts_file, 'r') as f:
                    data = json.load(f)
                    return [alert for alert in data.get('alerts', []) if alert.get('status') == 'active']
        except Exception as e:
            logging.error(f"❌ Failed to load alerts: {e}")
        
        return []
    
    def acknowledge_alert(self, alert_id: str, user_id: str) -> bool:
        """Mark an alert as acknowledged"""
        try:
            alerts_file = 'data/alerts.json'
            if not os.path.exists(alerts_file):
                return False
            
            with open(alerts_file, 'r') as f:
                data = json.load(f)
            
            # Find and update the alert
            for alert in data['alerts']:
                if alert['id'] == alert_id:
                    alert['acknowledged'] = True
                    alert['acknowledged_by'] = user_id
                    alert['acknowledged_at'] = datetime.now().isoformat()
                    break
            
            # Save updated alerts
            with open(alerts_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logging.info(f"✅ Alert {alert_id} acknowledged by {user_id}")
            return True
        
        except Exception as e:
            logging.error(f"❌ Failed to acknowledge alert: {e}")
            return False
    
    def resolve_alert(self, alert_id: str, user_id: str, resolution_notes: str = "") -> bool:
        """Mark an alert as resolved"""
        try:
            alerts_file = 'data/alerts.json'
            if not os.path.exists(alerts_file):
                return False
            
            with open(alerts_file, 'r') as f:
                data = json.load(f)
            
            # Find and update the alert
            for alert in data['alerts']:
                if alert['id'] == alert_id:
                    alert['status'] = 'resolved'
                    alert['resolved_by'] = user_id
                    alert['resolved_at'] = datetime.now().isoformat()
                    alert['resolution_notes'] = resolution_notes
                    break
            
            # Save updated alerts
            with open(alerts_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logging.info(f"✅ Alert {alert_id} resolved by {user_id}")
            return True
        
        except Exception as e:
            logging.error(f"❌ Failed to resolve alert: {e}")
            return False
    
    def _calculate_severity(self, value, threshold):
        """Calculate alert severity based on threshold"""
        ratio = value / threshold
        
        if ratio >= 2.0:
            return 'critical'
        elif ratio >= 1.5:
            return 'high'
        elif ratio >= 1.2:
            return 'moderate'
        else:
            return 'low'
    
    def _calculate_score(self, row, df, metric):
        """Calculate unified alert score (0-100)"""
        score = 0
        
        # Base score from current value
        if metric in row:
            threshold = self.thresholds.get(metric.replace('_', ''), 1.0)
            normalized_value = min(row[metric] / threshold, 2.0)  # Cap at 2x threshold
            score += normalized_value * 50 * self.weights['tide']
        
        # Trend score
        trend_score = self._calculate_trend_score(df, metric)
        score += trend_score * self.weights['trend']
        
        # Wind score (if available)
        if 'wind_speed' in row:
            wind_ratio = min(row['wind_speed'] / self.thresholds['wind'], 2.0)
            score += wind_ratio * 20 * self.weights['wind']
        
        # Reports score (mock - would be real in production)
        reports_score = 0  # Would calculate based on nearby reports
        score += reports_score * self.weights['reports']
        
        # ML score (mock - would be real ML prediction)
        ml_score = np.random.uniform(0, 30)  # Mock ML confidence
        score += ml_score * self.weights['ml']
        
        # Clamp to 0-100
        return max(0, min(100, score))
    
    def _calculate_trend_score(self, df, metric):
        """Calculate trend score based on recent changes"""
        if metric not in df.columns or len(df) < 4:
            return 0
        
        try:
            # Calculate 3-hour trend
            recent_avg = df[metric].tail(3).mean()
            prev_avg = df[metric].tail(6).head(3).mean()
            
            if prev_avg > 0:
                trend_ratio = (recent_avg - prev_avg) / prev_avg
                return max(0, min(20, trend_ratio * 20))
        except:
            pass
        
        return 0
    
    def detect_anomalies(self, df, metric):
        """Detect anomalies using statistical methods"""
        if metric not in df.columns:
            return []
        
        anomalies = []
        
        # Z-score method
        values = df[metric].dropna()
        if len(values) > 10:
            mean = values.mean()
            std = values.std()
            
            for idx, value in values.items():
                z_score = abs((value - mean) / std)
                if z_score > 3:  # 3-sigma rule
                    anomalies.append({
                        'index': idx,
                        'value': value,
                        'z_score': z_score,
                        'method': 'z_score'
                    })
        
        # Rolling mean method
        if len(values) > 20:
            rolling_mean = values.rolling(window=10, center=True).mean()
            rolling_std = values.rolling(window=10, center=True).std()
            
            for idx, value in values.items():
                if not pd.isna(rolling_mean[idx]) and not pd.isna(rolling_std[idx]):
                    if rolling_std[idx] > 0:
                        z_score = abs((value - rolling_mean[idx]) / rolling_std[idx])
                        if z_score > 2.5:  # More sensitive for rolling
                            anomalies.append({
                                'index': idx,
                                'value': value,
                                'z_score': z_score,
                                'method': 'rolling_mean'
                            })
        
        return anomalies
    
    def predict_threats(self, historical_data, forecast_hours=24):
        """Predict potential threats based on historical data"""
        predictions = []
        
        if historical_data is None or historical_data.empty:
            return predictions
        
        # Simple trend-based prediction
        for metric in ['tide_level', 'sea_level', 'wave_height', 'wind_speed']:
            if metric in historical_data.columns:
                recent_trend = self._calculate_trend(historical_data[metric])
                
                if abs(recent_trend) > 0.1:  # Significant trend
                    prediction = {
                        'metric': metric,
                        'trend': recent_trend,
                        'predicted_threat': recent_trend > 0,
                        'confidence': min(abs(recent_trend) * 10, 90),
                        'forecast_hours': forecast_hours
                    }
                    predictions.append(prediction)
        
        return predictions
    
    def _calculate_trend(self, series):
        """Calculate trend in time series"""
        if len(series) < 2:
            return 0
        
        # Simple linear trend
        x = np.arange(len(series))
        y = series.values
        
        if len(y) > 1:
            slope = np.polyfit(x, y, 1)[0]
            return slope
        return 0
    
    def get_alert_summary(self, alerts):
        """Generate summary of alerts"""
        if not alerts:
            return {
                'total_alerts': 0,
                'by_severity': {},
                'by_type': {},
                'avg_score': 0
            }
        
        summary = {
            'total_alerts': len(alerts),
            'by_severity': {},
            'by_type': {},
            'avg_score': np.mean([a['score'] for a in alerts])
        }
        
        # Count by severity
        for alert in alerts:
            severity = alert['severity']
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
        
        # Count by type
        for alert in alerts:
            alert_type = alert['type']
            summary['by_type'][alert_type] = summary['by_type'].get(alert_type, 0) + 1
        
        return summary
