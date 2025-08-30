"""
ML Models for Anomaly Detection

This module contains the machine learning models used for detecting various
types of anomalies in coastal monitoring data.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CoastalAnomalyDetector:
    """
    Main anomaly detection class for coastal monitoring data.
    
    Supports multiple anomaly detection algorithms and can handle
    various types of coastal data including sea level, wind speed,
    temperature, and water quality parameters.
    """
    
    def __init__(self, model_type: str = "isolation_forest", contamination: float = 0.05):
        """
        Initialize the anomaly detector.
        
        Args:
            model_type: Type of model to use ('isolation_forest', 'lstm')
            contamination: Expected proportion of anomalies in the data
        """
        self.model_type = model_type
        self.contamination = contamination
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = []
        self.is_trained = False
        
    def preprocess_data(self, df: pd.DataFrame, feature_columns: List[str]) -> pd.DataFrame:
        """
        Preprocess the data for anomaly detection.
        
        Args:
            df: Input DataFrame
            feature_columns: List of feature column names
            
        Returns:
            Preprocessed DataFrame
        """
        logger.info(f"Preprocessing data with {len(feature_columns)} features")
        
        # Store feature columns for later use
        self.feature_columns = feature_columns
        
        # Select only the feature columns
        data = df[feature_columns].copy()
        
        # Handle missing values
        data = data.fillna(method='ffill').fillna(method='bfill')
        
        # Remove outliers using IQR method
        for col in feature_columns:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]
        
        # Scale the features
        data_scaled = self.scaler.fit_transform(data)
        
        return pd.DataFrame(data_scaled, columns=feature_columns, index=data.index)
    
    def train_isolation_forest(self, df: pd.DataFrame, feature_columns: List[str]) -> None:
        """
        Train Isolation Forest model for anomaly detection.
        
        Args:
            df: Training DataFrame
            feature_columns: List of feature column names
        """
        logger.info("Training Isolation Forest model")
        
        # Preprocess data
        processed_data = self.preprocess_data(df, feature_columns)
        
        # Initialize and train Isolation Forest
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=42,
            n_estimators=100
        )
        
        self.model.fit(processed_data)
        self.is_trained = True
        logger.info("Isolation Forest model trained successfully")
    
    def train_lstm_model(self, df: pd.DataFrame, feature_columns: List[str], 
                        sequence_length: int = 10) -> None:
        """
        Train LSTM model for time-series anomaly detection.
        
        Args:
            df: Training DataFrame
            feature_columns: List of feature column names
            sequence_length: Length of input sequences
        """
        logger.info("Training LSTM model")
        
        # This is a simplified LSTM implementation
        # In a production environment, you might want to use TensorFlow/Keras
        
        # Preprocess data
        processed_data = self.preprocess_data(df, feature_columns)
        
        # Create sequences for LSTM
        sequences = []
        for i in range(len(processed_data) - sequence_length):
            sequences.append(processed_data.iloc[i:i+sequence_length].values)
        
        sequences = np.array(sequences)
        
        # For now, we'll use a simple autoencoder approach
        # In practice, you'd implement a proper LSTM autoencoder
        from sklearn.decomposition import PCA
        
        # Flatten sequences and use PCA for dimensionality reduction
        flattened_sequences = sequences.reshape(sequences.shape[0], -1)
        self.model = PCA(n_components=0.95)  # Keep 95% of variance
        self.model.fit(flattened_sequences)
        
        self.is_trained = True
        logger.info("LSTM model trained successfully")
    
    def train(self, df: pd.DataFrame, feature_columns: List[str], **kwargs) -> None:
        """
        Train the anomaly detection model.
        
        Args:
            df: Training DataFrame
            feature_columns: List of feature column names
            **kwargs: Additional arguments for specific model types
        """
        if self.model_type == "isolation_forest":
            self.train_isolation_forest(df, feature_columns)
        elif self.model_type == "lstm":
            sequence_length = kwargs.get('sequence_length', 10)
            self.train_lstm_model(df, feature_columns, sequence_length)
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")
    
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """
        Predict anomalies in the given data.
        
        Args:
            data: Input DataFrame
            
        Returns:
            Array of predictions (-1 for anomaly, 1 for normal)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Select and preprocess features
        if len(self.feature_columns) > 0:
            data = data[self.feature_columns]
        
        # Scale the data
        data_scaled = self.scaler.transform(data)
        
        if self.model_type == "isolation_forest":
            return self.model.predict(data_scaled)
        elif self.model_type == "lstm":
            # For LSTM, we need to create sequences
            # This is a simplified implementation
            return self.model.predict(data_scaled)
    
    def predict_single(self, **kwargs) -> Dict[str, any]:
        """
        Predict anomaly for a single data point.
        
        Args:
            **kwargs: Feature values (e.g., sea_level=1.5, wind_speed=25.0)
            
        Returns:
            Dictionary with prediction results
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Create DataFrame from input features
        data = pd.DataFrame([kwargs])
        
        # Ensure all required features are present
        missing_features = set(self.feature_columns) - set(data.columns)
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")
        
        # Make prediction
        prediction = self.predict(data)
        
        return {
            "is_anomaly": prediction[0] == -1,
            "threat_level": "High" if prediction[0] == -1 else "Low",
            "confidence": 0.95,  # Placeholder confidence score
            "features": kwargs
        }
    
    def save_model(self, filepath: str) -> None:
        """
        Save the trained model to disk.
        
        Args:
            filepath: Path where to save the model
        """
        if not self.is_trained:
            raise ValueError("No trained model to save")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'model_type': self.model_type,
            'contamination': self.contamination
        }
        
        joblib.dump(model_data, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str) -> None:
        """
        Load a trained model from disk.
        
        Args:
            filepath: Path to the saved model
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']
        self.model_type = model_data['model_type']
        self.contamination = model_data['contamination']
        self.is_trained = True
        
        logger.info(f"Model loaded from {filepath}")


class StormSurgeDetector(CoastalAnomalyDetector):
    """
    Specialized detector for storm surge anomalies.
    """
    
    def __init__(self):
        super().__init__(model_type="isolation_forest", contamination=0.03)
        self.default_features = ["sea_level", "wind_speed", "atmospheric_pressure", "wave_height"]
    
    def train(self, df: pd.DataFrame, feature_columns: Optional[List[str]] = None) -> None:
        """
        Train storm surge detector with default features if none specified.
        """
        if feature_columns is None:
            feature_columns = [col for col in self.default_features if col in df.columns]
        
        super().train(df, feature_columns)


class WaterQualityDetector(CoastalAnomalyDetector):
    """
    Specialized detector for water quality anomalies (illegal dumping detection).
    """
    
    def __init__(self):
        super().__init__(model_type="isolation_forest", contamination=0.05)
        self.default_features = ["ph", "turbidity", "dissolved_oxygen", "temperature", "conductivity"]
    
    def train(self, df: pd.DataFrame, feature_columns: Optional[List[str]] = None) -> None:
        """
        Train water quality detector with default features if none specified.
        """
        if feature_columns is None:
            feature_columns = [col for col in self.default_features if col in df.columns]
        
        super().train(df, feature_columns)
