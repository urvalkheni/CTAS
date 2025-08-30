import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid

class AlertEngine:
    def __init__(self):
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
    
    def update_thresholds(self, new_thresholds):
        """Update alert thresholds"""
        self.thresholds.update(new_thresholds)
    
    def process_sensor_data(self, df):
        """Process sensor data and generate alerts"""
        alerts = []
        
        if df is None or df.empty:
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
        
        return alerts
    
    def _analyze_row(self, row, df):
        """Analyze a single row for potential alerts"""
        alert = None
        
        # Check tide level
        if 'tide_level' in row and row['tide_level'] > self.thresholds['tide']:
            alert = self._create_alert(
                type="storm_surge",
                severity=self._calculate_severity(row['tide_level'], self.thresholds['tide']),
                message=f"🚨 High tide detected: {row['tide_level']:.1f}m (threshold: {self.thresholds['tide']}m)",
                location={'type': 'Point', 'coordinates': [72.8777, 19.0760]},  # Mumbai
                score=self._calculate_score(row, df, 'tide_level')
            )
        
        # Check sea level
        elif 'sea_level' in row and row['sea_level'] > self.thresholds['sea_level']:
            alert = self._create_alert(
                type="sea_level_rise",
                severity=self._calculate_severity(row['sea_level'], self.thresholds['sea_level']),
                message=f"⚠️ Elevated sea level: {row['sea_level']:.1f}m (threshold: {self.thresholds['sea_level']}m)",
                location={'type': 'Point', 'coordinates': [72.8777, 19.0760]},
                score=self._calculate_score(row, df, 'sea_level')
            )
        
        # Check wave height
        elif 'wave_height' in row and row['wave_height'] > self.thresholds['wave']:
            alert = self._create_alert(
                type="high_waves",
                severity=self._calculate_severity(row['wave_height'], self.thresholds['wave']),
                message=f"🌊 High waves detected: {row['wave_height']:.1f}m (threshold: {self.thresholds['wave']}m)",
                location={'type': 'Point', 'coordinates': [72.8777, 19.0760]},
                score=self._calculate_score(row, df, 'wave_height')
            )
        
        # Check wind speed
        elif 'wind_speed' in row and row['wind_speed'] > self.thresholds['wind']:
            alert = self._create_alert(
                type="high_winds",
                severity=self._calculate_severity(row['wind_speed'], self.thresholds['wind']),
                message=f"💨 High wind speed: {row['wind_speed']:.1f} km/h (threshold: {self.thresholds['wind']} km/h)",
                location={'type': 'Point', 'coordinates': [72.8777, 19.0760]},
                score=self._calculate_score(row, df, 'wind_speed')
            )
        
        # Check turbidity
        elif 'turbidity' in row and row['turbidity'] > self.thresholds['turbidity']:
            alert = self._create_alert(
                type="water_pollution",
                severity=self._calculate_severity(row['turbidity'], self.thresholds['turbidity']),
                message=f"🌊 High turbidity detected: {row['turbidity']:.1f} NTU (threshold: {self.thresholds['turbidity']} NTU)",
                location={'type': 'Point', 'coordinates': [72.8777, 19.0760]},
                score=self._calculate_score(row, df, 'turbidity')
            )
        
        return alert
    
    def _create_alert(self, type, severity, message, location, score):
        """Create alert object"""
        return {
            'type': type,
            'severity': severity,
            'message': message,
            'location': location,
            'score': score,
            'createdAt': datetime.now().isoformat(),
            'evidence': []
        }
    
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
