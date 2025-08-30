import numpy as np
import random
from datetime import datetime
import os

class MLService:
    def __init__(self):
        # Mock model parameters
        self.models = {
            'mangrove_detection': {
                'accuracy': 0.85,
                'version': '1.0.0',
                'last_updated': datetime.now().isoformat()
            },
            'anomaly_detection': {
                'accuracy': 0.78,
                'version': '1.0.0',
                'last_updated': datetime.now().isoformat()
            }
        }
    
    def validate_image(self, image_path):
        """Validate mangrove image and return confidence score"""
        # Mock image validation
        # In production, this would use YOLOv8 or similar model
        
        # Simple heuristic based on filename
        filename = os.path.basename(image_path).lower()
        
        if 'cut' in filename or 'cleared' in filename:
            # High confidence for cut mangrove
            confidence = random.uniform(85, 95)
            return confidence
        elif 'healthy' in filename or 'green' in filename:
            # High confidence for healthy mangrove
            confidence = random.uniform(80, 90)
            return confidence
        else:
            # Random confidence for unknown images
            confidence = random.uniform(60, 85)
            return confidence
    
    def detect_mangrove_health(self, image_path):
        """Detect mangrove health status from image"""
        confidence = self.validate_image(image_path)
        
        # Determine status based on confidence
        if confidence > 80:
            status = "healthy"
        elif confidence > 60:
            status = "degraded"
        else:
            status = "cut"
        
        return {
            'status': status,
            'confidence': confidence,
            'tags': self._generate_tags(image_path),
            'model_version': self.models['mangrove_detection']['version']
        }
    
    def _generate_tags(self, image_path):
        """Generate tags for the image"""
        # Mock tag generation
        possible_tags = [
            'mangrove', 'coastal', 'vegetation', 'water', 'trees',
            'cleared', 'healthy', 'degraded', 'shoreline', 'conservation'
        ]
        
        # Select random tags
        num_tags = random.randint(2, 5)
        tags = random.sample(possible_tags, num_tags)
        
        return tags
    
    def detect_anomalies(self, time_series_data, metric):
        """Detect anomalies in time series data"""
        if not time_series_data or len(time_series_data) < 10:
            return []
        
        anomalies = []
        
        # Convert to numpy array
        data = np.array(time_series_data)
        
        # Z-score method
        mean = np.mean(data)
        std = np.std(data)
        
        if std > 0:
            z_scores = np.abs((data - mean) / std)
            anomaly_indices = np.where(z_scores > 2.5)[0]
            
            for idx in anomaly_indices:
                anomalies.append({
                    'index': int(idx),
                    'value': float(data[idx]),
                    'z_score': float(z_scores[idx]),
                    'method': 'z_score',
                    'confidence': min(z_scores[idx] * 10, 95)
                })
        
        # Isolation Forest simulation (mock)
        if len(data) > 20:
            # Simulate isolation forest results
            num_anomalies = random.randint(0, min(3, len(data) // 10))
            if num_anomalies > 0:
                anomaly_indices = random.sample(range(len(data)), num_anomalies)
                
                for idx in anomaly_indices:
                    if idx not in [a['index'] for a in anomalies]:
                        anomalies.append({
                            'index': idx,
                            'value': float(data[idx]),
                            'z_score': random.uniform(2.0, 4.0),
                            'method': 'isolation_forest',
                            'confidence': random.uniform(70, 95)
                        })
        
        return anomalies
    
    def predict_sequence(self, historical_data, forecast_steps=24):
        """Predict future values in time series"""
        if not historical_data or len(historical_data) < 10:
            return []
        
        data = np.array(historical_data)
        
        # Simple trend-based prediction
        if len(data) >= 2:
            # Calculate trend
            x = np.arange(len(data))
            slope, intercept = np.polyfit(x, data, 1)
            
            # Generate predictions
            future_x = np.arange(len(data), len(data) + forecast_steps)
            predictions = slope * future_x + intercept
            
            # Add some noise
            noise = np.random.normal(0, np.std(data) * 0.1, forecast_steps)
            predictions += noise
            
            return [
                {
                    'step': i,
                    'predicted_value': float(predictions[i]),
                    'confidence': max(50, 95 - i * 2),  # Decreasing confidence
                    'timestamp': datetime.now().isoformat()  # Would be actual timestamp
                }
                for i in range(forecast_steps)
            ]
        
        return []
    
    def classify_report_type(self, description, image_path=None):
        """Classify report type based on description and optional image"""
        # Mock classification
        description_lower = description.lower()
        
        # Simple keyword-based classification
        if any(word in description_lower for word in ['cut', 'cleared', 'removed', 'destroyed']):
            return {
                'type': 'mangrove_cut',
                'confidence': random.uniform(80, 95),
                'keywords': ['cut', 'cleared', 'removed']
            }
        elif any(word in description_lower for word in ['dump', 'waste', 'garbage', 'trash']):
            return {
                'type': 'dumping',
                'confidence': random.uniform(75, 90),
                'keywords': ['dump', 'waste', 'garbage']
            }
        elif any(word in description_lower for word in ['pollution', 'contamination', 'oil', 'chemical']):
            return {
                'type': 'pollution',
                'confidence': random.uniform(70, 85),
                'keywords': ['pollution', 'contamination']
            }
        elif any(word in description_lower for word in ['illegal', 'unauthorized', 'fishing', 'construction']):
            return {
                'type': 'illegal_activity',
                'confidence': random.uniform(65, 80),
                'keywords': ['illegal', 'unauthorized']
            }
        else:
            return {
                'type': 'other',
                'confidence': random.uniform(50, 70),
                'keywords': []
            }
    
    def extract_features(self, image_path):
        """Extract features from image for analysis"""
        # Mock feature extraction
        # In production, this would use CNN or other feature extraction methods
        
        features = {
            'vegetation_coverage': random.uniform(0, 1),
            'water_presence': random.uniform(0, 1),
            'human_activity': random.uniform(0, 1),
            'image_quality': random.uniform(0.5, 1),
            'dominant_colors': self._extract_dominant_colors(),
            'texture_features': self._extract_texture_features()
        }
        
        return features
    
    def _extract_dominant_colors(self):
        """Mock dominant color extraction"""
        colors = ['green', 'blue', 'brown', 'gray', 'white']
        return random.sample(colors, random.randint(2, 4))
    
    def _extract_texture_features(self):
        """Mock texture feature extraction"""
        return {
            'smoothness': random.uniform(0, 1),
            'contrast': random.uniform(0, 1),
            'homogeneity': random.uniform(0, 1)
        }
    
    def get_model_info(self):
        """Get information about deployed models"""
        return {
            'models': self.models,
            'total_models': len(self.models),
            'last_updated': datetime.now().isoformat(),
            'status': 'operational'
        }
    
    def retrain_model(self, model_name, training_data):
        """Retrain a model with new data"""
        # Mock retraining
        if model_name in self.models:
            self.models[model_name]['last_updated'] = datetime.now().isoformat()
            self.models[model_name]['accuracy'] += random.uniform(-0.05, 0.05)
            
            return {
                'model_name': model_name,
                'status': 'retrained',
                'new_accuracy': self.models[model_name]['accuracy'],
                'training_samples': len(training_data) if training_data else 0,
                'retrained_at': datetime.now().isoformat()
            }
        
        return None
    
    def validate_model_performance(self, model_name, test_data):
        """Validate model performance on test data"""
        if model_name not in self.models:
            return None
        
        # Mock performance metrics
        performance = {
            'model_name': model_name,
            'accuracy': random.uniform(0.7, 0.95),
            'precision': random.uniform(0.65, 0.9),
            'recall': random.uniform(0.6, 0.85),
            'f1_score': random.uniform(0.65, 0.9),
            'test_samples': len(test_data) if test_data else 0,
            'validated_at': datetime.now().isoformat()
        }
        
        return performance
