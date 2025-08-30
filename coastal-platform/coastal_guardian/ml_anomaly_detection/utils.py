"""
Utility Functions for Coastal Anomaly Detection

This module provides utility functions for data generation, model evaluation,
and various helper functions used throughout the anomaly detection system.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import logging
from datetime import datetime, timedelta
import random
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_sample_data(n_samples: int = 1000, data_type: str = "storm_surge") -> pd.DataFrame:
    """
    Generate sample data for testing and demonstration purposes.
    
    Args:
        n_samples: Number of samples to generate
        data_type: Type of data to generate ('storm_surge', 'water_quality', 'mixed')
        
    Returns:
        DataFrame with generated sample data
    """
    logger.info(f"Generating {n_samples} samples of {data_type} data")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Generate timestamps
    start_date = datetime.now() - timedelta(days=30)
    timestamps = [start_date + timedelta(hours=i) for i in range(n_samples)]
    
    if data_type == "storm_surge":
        return _generate_storm_surge_data(timestamps)
    elif data_type == "water_quality":
        return _generate_water_quality_data(timestamps)
    elif data_type == "mixed":
        return _generate_mixed_data(timestamps)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")


def _generate_storm_surge_data(timestamps: List[datetime]) -> pd.DataFrame:
    """Generate storm surge sample data."""
    n_samples = len(timestamps)
    
    # Base values
    base_sea_level = 1.0  # meters
    base_wind_speed = 10.0  # m/s
    base_pressure = 1013.25  # hPa
    base_wave_height = 0.5  # meters
    
    # Generate normal conditions with some variation
    sea_level = np.random.normal(base_sea_level, 0.2, n_samples)
    wind_speed = np.random.normal(base_wind_speed, 3.0, n_samples)
    atmospheric_pressure = np.random.normal(base_pressure, 5.0, n_samples)
    wave_height = np.random.normal(base_wave_height, 0.3, n_samples)
    
    # Add some anomalies (storm conditions)
    anomaly_indices = random.sample(range(n_samples), n_samples // 20)  # 5% anomalies
    
    for idx in anomaly_indices:
        # Storm surge conditions
        sea_level[idx] = np.random.uniform(2.0, 4.0)  # High sea level
        wind_speed[idx] = np.random.uniform(25.0, 50.0)  # High wind speed
        atmospheric_pressure[idx] = np.random.uniform(980.0, 1000.0)  # Low pressure
        wave_height[idx] = np.random.uniform(2.0, 5.0)  # High waves
    
    # Ensure non-negative values
    sea_level = np.maximum(sea_level, 0.0)
    wind_speed = np.maximum(wind_speed, 0.0)
    wave_height = np.maximum(wave_height, 0.0)
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'sea_level': sea_level,
        'wind_speed': wind_speed,
        'atmospheric_pressure': atmospheric_pressure,
        'wave_height': wave_height
    })


def _generate_water_quality_data(timestamps: List[datetime]) -> pd.DataFrame:
    """Generate water quality sample data."""
    n_samples = len(timestamps)
    
    # Base values
    base_ph = 7.5
    base_turbidity = 2.0  # NTU
    base_dissolved_oxygen = 8.0  # mg/L
    base_temperature = 20.0  # Celsius
    base_conductivity = 500.0  # mS/cm
    
    # Generate normal conditions
    ph = np.random.normal(base_ph, 0.5, n_samples)
    turbidity = np.random.normal(base_turbidity, 1.0, n_samples)
    dissolved_oxygen = np.random.normal(base_dissolved_oxygen, 1.0, n_samples)
    temperature = np.random.normal(base_temperature, 3.0, n_samples)
    conductivity = np.random.normal(base_conductivity, 100.0, n_samples)
    
    # Add some anomalies (pollution events)
    anomaly_indices = random.sample(range(n_samples), n_samples // 15)  # ~7% anomalies
    
    for idx in anomaly_indices:
        # Pollution conditions
        ph[idx] = np.random.uniform(4.0, 6.0)  # Acidic water
        turbidity[idx] = np.random.uniform(15.0, 30.0)  # High turbidity
        dissolved_oxygen[idx] = np.random.uniform(2.0, 4.0)  # Low oxygen
        temperature[idx] = np.random.uniform(25.0, 35.0)  # High temperature
        conductivity[idx] = np.random.uniform(800.0, 1500.0)  # High conductivity
    
    # Ensure realistic ranges
    ph = np.clip(ph, 0.0, 14.0)
    turbidity = np.maximum(turbidity, 0.0)
    dissolved_oxygen = np.maximum(dissolved_oxygen, 0.0)
    conductivity = np.maximum(conductivity, 0.0)
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'ph': ph,
        'turbidity': turbidity,
        'dissolved_oxygen': dissolved_oxygen,
        'temperature': temperature,
        'conductivity': conductivity
    })


def _generate_mixed_data(timestamps: List[datetime]) -> pd.DataFrame:
    """Generate mixed coastal data."""
    storm_data = _generate_storm_surge_data(timestamps)
    water_data = _generate_water_quality_data(timestamps)
    
    # Combine the data
    mixed_data = pd.concat([storm_data, water_data.drop('timestamp', axis=1)], axis=1)
    
    return mixed_data


def evaluate_model_performance(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Evaluate model performance for anomaly detection.
    
    Args:
        y_true: True labels (1 for normal, -1 for anomaly)
        y_pred: Predicted labels (1 for normal, -1 for anomaly)
        
    Returns:
        Dictionary with performance metrics
    """
    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
    
    # Convert to binary classification (0 for normal, 1 for anomaly)
    y_true_binary = (y_true == -1).astype(int)
    y_pred_binary = (y_pred == -1).astype(int)
    
    # Calculate metrics
    precision = precision_score(y_true_binary, y_pred_binary, zero_division=0)
    recall = recall_score(y_true_binary, y_pred_binary, zero_division=0)
    f1 = f1_score(y_true_binary, y_pred_binary, zero_division=0)
    accuracy = accuracy_score(y_true_binary, y_pred_binary)
    
    # Calculate anomaly detection rate
    anomaly_rate = np.mean(y_pred_binary)
    true_anomaly_rate = np.mean(y_true_binary)
    
    return {
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'accuracy': accuracy,
        'anomaly_detection_rate': anomaly_rate,
        'true_anomaly_rate': true_anomaly_rate
    }


def create_anomaly_labels(df: pd.DataFrame, method: str = "threshold") -> np.ndarray:
    """
    Create anomaly labels for evaluation purposes.
    
    Args:
        df: Input DataFrame
        method: Method for creating labels ('threshold', 'statistical')
        
    Returns:
        Array of labels (1 for normal, -1 for anomaly)
    """
    if method == "threshold":
        return _create_threshold_labels(df)
    elif method == "statistical":
        return _create_statistical_labels(df)
    else:
        raise ValueError(f"Unsupported method: {method}")


def _create_threshold_labels(df: pd.DataFrame) -> np.ndarray:
    """Create labels based on threshold values."""
    labels = np.ones(len(df))  # Start with all normal
    
    # Define thresholds for different features
    thresholds = {
        'sea_level': 2.0,
        'wind_speed': 25.0,
        'atmospheric_pressure': 1000.0,
        'wave_height': 2.0,
        'ph': 6.0,
        'turbidity': 10.0,
        'dissolved_oxygen': 4.0,
        'temperature': 30.0,
        'conductivity': 800.0
    }
    
    for feature, threshold in thresholds.items():
        if feature in df.columns:
            if feature in ['atmospheric_pressure']:
                # Lower pressure indicates storm
                anomaly_mask = df[feature] < threshold
            else:
                # Higher values indicate anomalies
                anomaly_mask = df[feature] > threshold
            
            labels[anomaly_mask] = -1
    
    return labels


def _create_statistical_labels(df: pd.DataFrame) -> np.ndarray:
    """Create labels based on statistical outliers."""
    labels = np.ones(len(df))  # Start with all normal
    
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numerical_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Mark outliers as anomalies
        outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        labels[outlier_mask] = -1
    
    return labels


def save_sample_data(data: pd.DataFrame, filename: str, data_dir: str = "sample_data") -> str:
    """
    Save sample data to CSV file.
    
    Args:
        data: DataFrame to save
        filename: Name of the file
        data_dir: Directory to save the file
        
    Returns:
        Path to the saved file
    """
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, filename)
    data.to_csv(filepath, index=False)
    logger.info(f"Sample data saved to {filepath}")
    return filepath


def load_sample_data(filename: str, data_dir: str = "sample_data") -> pd.DataFrame:
    """
    Load sample data from CSV file.
    
    Args:
        filename: Name of the file to load
        data_dir: Directory containing the file
        
    Returns:
        Loaded DataFrame
    """
    filepath = os.path.join(data_dir, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    data = pd.read_csv(filepath)
    logger.info(f"Sample data loaded from {filepath}")
    return data


def create_training_pipeline(data_type: str = "storm_surge") -> Dict[str, Any]:
    """
    Create a complete training pipeline configuration.
    
    Args:
        data_type: Type of data to configure for
        
    Returns:
        Dictionary with pipeline configuration
    """
    if data_type == "storm_surge":
        return {
            'model_type': 'isolation_forest',
            'contamination': 0.03,
            'feature_columns': ['sea_level', 'wind_speed', 'atmospheric_pressure', 'wave_height'],
            'scaling_method': 'robust',
            'outlier_method': 'iqr'
        }
    elif data_type == "water_quality":
        return {
            'model_type': 'isolation_forest',
            'contamination': 0.05,
            'feature_columns': ['ph', 'turbidity', 'dissolved_oxygen', 'temperature', 'conductivity'],
            'scaling_method': 'standard',
            'outlier_method': 'iqr'
        }
    elif data_type == "mixed":
        return {
            'model_type': 'isolation_forest',
            'contamination': 0.04,
            'feature_columns': ['sea_level', 'wind_speed', 'ph', 'turbidity', 'temperature'],
            'scaling_method': 'standard',
            'outlier_method': 'iqr'
        }
    else:
        raise ValueError(f"Unsupported data type: {data_type}")


def generate_alert_message(anomaly_type: str, severity: str, details: Dict[str, Any]) -> str:
    """
    Generate human-readable alert messages for anomalies.
    
    Args:
        anomaly_type: Type of anomaly detected
        severity: Severity level ('Low', 'Medium', 'High', 'Critical')
        details: Dictionary with anomaly details
        
    Returns:
        Formatted alert message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if anomaly_type == "storm_surge":
        return f"""
🚨 STORM SURGE ALERT - {severity.upper()} 🚨
Time: {timestamp}

Sea Level: {details.get('sea_level', 'N/A')} meters
Wind Speed: {details.get('wind_speed', 'N/A')} m/s
Atmospheric Pressure: {details.get('atmospheric_pressure', 'N/A')} hPa
Wave Height: {details.get('wave_height', 'N/A')} meters

RECOMMENDATIONS:
- Monitor weather updates
- Secure loose objects
- Evacuate low-lying areas if necessary
- Follow emergency protocols
        """.strip()
    
    elif anomaly_type == "water_quality":
        return f"""
🌊 WATER QUALITY ALERT - {severity.upper()} 🌊
Time: {timestamp}

pH Level: {details.get('ph', 'N/A')}
Turbidity: {details.get('turbidity', 'N/A')} NTU
Dissolved Oxygen: {details.get('dissolved_oxygen', 'N/A')} mg/L
Temperature: {details.get('temperature', 'N/A')}°C
Conductivity: {details.get('conductivity', 'N/A')} mS/cm

RECOMMENDATIONS:
- Collect water samples for analysis
- Investigate potential pollution sources
- Monitor aquatic life
- Check nearby industrial discharges
        """.strip()
    
    else:
        return f"""
⚠️ ANOMALY DETECTED - {severity.upper()} ⚠️
Time: {timestamp}
Type: {anomaly_type}

Details: {details}

Please investigate the detected anomaly.
        """.strip()


def validate_input_data(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """
    Validate input data for required columns and data types.
    
    Args:
        df: Input DataFrame
        required_columns: List of required column names
        
    Returns:
        True if validation passes, False otherwise
    """
    # Check if all required columns are present
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        logger.error(f"Missing required columns: {missing_columns}")
        return False
    
    # Check for non-numeric data in required columns
    for col in required_columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            logger.error(f"Column {col} is not numeric")
            return False
    
    # Check for all-null columns
    for col in required_columns:
        if df[col].isnull().all():
            logger.error(f"Column {col} contains only null values")
            return False
    
    logger.info("Input data validation passed")
    return True


def calculate_confidence_score(prediction: int, feature_values: Dict[str, float]) -> float:
    """
    Calculate confidence score for a prediction based on feature values.
    
    Args:
        prediction: Model prediction (-1 for anomaly, 1 for normal)
        feature_values: Dictionary of feature values
        
    Returns:
        Confidence score between 0 and 1
    """
    # Base confidence
    base_confidence = 0.8
    
    # Adjust confidence based on feature values
    adjustments = []
    
    # Storm surge features
    if 'sea_level' in feature_values:
        sea_level = feature_values['sea_level']
        if sea_level > 3.0:
            adjustments.append(0.1)  # High confidence for extreme values
        elif sea_level > 2.0:
            adjustments.append(0.05)
    
    if 'wind_speed' in feature_values:
        wind_speed = feature_values['wind_speed']
        if wind_speed > 40.0:
            adjustments.append(0.1)
        elif wind_speed > 25.0:
            adjustments.append(0.05)
    
    # Water quality features
    if 'ph' in feature_values:
        ph = feature_values['ph']
        if ph < 5.0 or ph > 9.0:
            adjustments.append(0.1)
        elif ph < 6.0 or ph > 8.0:
            adjustments.append(0.05)
    
    if 'turbidity' in feature_values:
        turbidity = feature_values['turbidity']
        if turbidity > 20.0:
            adjustments.append(0.1)
        elif turbidity > 10.0:
            adjustments.append(0.05)
    
    # Calculate final confidence
    confidence = base_confidence + sum(adjustments)
    return min(confidence, 1.0)  # Cap at 1.0
