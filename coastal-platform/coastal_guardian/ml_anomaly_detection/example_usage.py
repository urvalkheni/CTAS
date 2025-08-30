"""
Example Usage of Coastal Anomaly Detection System

This script demonstrates how to use the anomaly detection system
for training models and making predictions on coastal monitoring data.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging

# Import our modules
from models import CoastalAnomalyDetector, StormSurgeDetector, WaterQualityDetector
from data_processor import CoastalDataProcessor, StormSurgeDataProcessor, WaterQualityDataProcessor
from utils import generate_sample_data, evaluate_model_performance, create_anomaly_labels, generate_alert_message

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def example_storm_surge_detection():
    """Example of storm surge anomaly detection."""
    logger.info("=== Storm Surge Anomaly Detection Example ===")
    
    # Generate sample storm surge data
    storm_data = generate_sample_data(n_samples=1000, data_type="storm_surge")
    logger.info(f"Generated {len(storm_data)} storm surge data points")
    
    # Initialize storm surge detector
    detector = StormSurgeDetector()
    
    # Define feature columns
    feature_columns = ['sea_level', 'wind_speed', 'atmospheric_pressure', 'wave_height']
    
    # Train the model
    logger.info("Training storm surge detector...")
    detector.train(storm_data, feature_columns)
    
    # Make some predictions
    logger.info("Making predictions...")
    
    # Normal conditions
    normal_prediction = detector.predict_single(
        sea_level=1.2,
        wind_speed=12.0,
        atmospheric_pressure=1012.0,
        wave_height=0.8
    )
    logger.info(f"Normal conditions prediction: {normal_prediction}")
    
    # Storm conditions
    storm_prediction = detector.predict_single(
        sea_level=3.5,
        wind_speed=45.0,
        atmospheric_pressure=985.0,
        wave_height=4.2
    )
    logger.info(f"Storm conditions prediction: {storm_prediction}")
    
    # Generate alert for storm prediction
    if storm_prediction["is_anomaly"]:
        alert = generate_alert_message(
            "storm_surge",
            "High",
            storm_prediction["features"]
        )
        logger.info(f"Alert generated:\n{alert}")
    
    # Save the model
    detector.save_model("models/storm_surge_model.pkl")
    logger.info("Storm surge model saved")


def example_water_quality_detection():
    """Example of water quality anomaly detection."""
    logger.info("=== Water Quality Anomaly Detection Example ===")
    
    # Generate sample water quality data
    water_data = generate_sample_data(n_samples=1000, data_type="water_quality")
    logger.info(f"Generated {len(water_data)} water quality data points")
    
    # Initialize water quality detector
    detector = WaterQualityDetector()
    
    # Define feature columns
    feature_columns = ['ph', 'turbidity', 'dissolved_oxygen', 'temperature', 'conductivity']
    
    # Train the model
    logger.info("Training water quality detector...")
    detector.train(water_data, feature_columns)
    
    # Make some predictions
    logger.info("Making predictions...")
    
    # Normal conditions
    normal_prediction = detector.predict_single(
        ph=7.2,
        turbidity=3.0,
        dissolved_oxygen=8.5,
        temperature=22.0,
        conductivity=450.0
    )
    logger.info(f"Normal conditions prediction: {normal_prediction}")
    
    # Pollution conditions
    pollution_prediction = detector.predict_single(
        ph=5.2,
        turbidity=25.0,
        dissolved_oxygen=3.0,
        temperature=32.0,
        conductivity=1200.0
    )
    logger.info(f"Pollution conditions prediction: {pollution_prediction}")
    
    # Generate alert for pollution prediction
    if pollution_prediction["is_anomaly"]:
        alert = generate_alert_message(
            "water_quality",
            "High",
            pollution_prediction["features"]
        )
        logger.info(f"Alert generated:\n{alert}")
    
    # Save the model
    detector.save_model("models/water_quality_model.pkl")
    logger.info("Water quality model saved")


def example_data_processing():
    """Example of data processing pipeline."""
    logger.info("=== Data Processing Example ===")
    
    # Generate mixed data
    mixed_data = generate_sample_data(n_samples=500, data_type="mixed")
    logger.info(f"Generated {len(mixed_data)} mixed data points")
    
    # Initialize data processor
    processor = CoastalDataProcessor(scaling_method="standard")
    
    # Define feature columns
    feature_columns = ['sea_level', 'wind_speed', 'ph', 'turbidity', 'temperature']
    
    # Process the data
    logger.info("Processing data...")
    processed_data, _ = processor.prepare_training_data(mixed_data, feature_columns)
    
    logger.info(f"Original data shape: {mixed_data.shape}")
    logger.info(f"Processed data shape: {processed_data.shape}")
    logger.info(f"Feature columns: {processor.feature_columns}")
    
    # Calculate feature importance
    importance_scores = processor.get_feature_importance(mixed_data, feature_columns)
    logger.info("Feature importance scores:")
    for feature, score in importance_scores.items():
        logger.info(f"  {feature}: {score:.4f}")
    
    # Save the processor
    processor.save_processor("models/data_processor.pkl")
    logger.info("Data processor saved")


def example_batch_predictions():
    """Example of batch predictions."""
    logger.info("=== Batch Predictions Example ===")
    
    # Load or generate data
    storm_data = generate_sample_data(n_samples=100, data_type="storm_surge")
    
    # Initialize detector
    detector = StormSurgeDetector()
    feature_columns = ['sea_level', 'wind_speed', 'atmospheric_pressure', 'wave_height']
    
    # Train the model
    detector.train(storm_data, feature_columns)
    
    # Create batch data for prediction
    batch_data = pd.DataFrame({
        'sea_level': [1.0, 2.5, 3.8, 0.8, 2.2],
        'wind_speed': [10.0, 30.0, 50.0, 8.0, 25.0],
        'atmospheric_pressure': [1013.0, 1000.0, 980.0, 1015.0, 995.0],
        'wave_height': [0.5, 2.0, 4.5, 0.3, 1.8]
    })
    
    # Make batch predictions
    predictions = detector.predict(batch_data)
    
    logger.info("Batch predictions:")
    for i, (_, row) in enumerate(batch_data.iterrows()):
        is_anomaly = predictions[i] == -1
        status = "ANOMALY" if is_anomaly else "Normal"
        logger.info(f"Sample {i+1}: {status} - Sea Level: {row['sea_level']:.1f}m, Wind: {row['wind_speed']:.1f}m/s")


def example_model_evaluation():
    """Example of model evaluation."""
    logger.info("=== Model Evaluation Example ===")
    
    # Generate data with known anomalies
    data = generate_sample_data(n_samples=1000, data_type="storm_surge")
    
    # Create true labels using threshold method
    true_labels = create_anomaly_labels(data, method="threshold")
    
    # Initialize and train detector
    detector = StormSurgeDetector()
    feature_columns = ['sea_level', 'wind_speed', 'atmospheric_pressure', 'wave_height']
    detector.train(data, feature_columns)
    
    # Make predictions
    predictions = detector.predict(data[feature_columns])
    
    # Evaluate performance
    metrics = evaluate_model_performance(true_labels, predictions)
    
    logger.info("Model Performance Metrics:")
    for metric, value in metrics.items():
        logger.info(f"  {metric}: {value:.4f}")


def example_api_integration():
    """Example of how the API would be used."""
    logger.info("=== API Integration Example ===")
    
    # Simulate API requests
    import requests
    import json
    
    # Example API endpoints (assuming the API is running)
    base_url = "http://localhost:8000"
    
    # Health check
    try:
        response = requests.get(f"{base_url}/health")
        logger.info(f"Health check: {response.json()}")
    except requests.exceptions.ConnectionError:
        logger.info("API not running - this is expected for this example")
        return
    
    # Example prediction request
    prediction_data = {
        "sea_level": 2.8,
        "wind_speed": 35.0,
        "atmospheric_pressure": 990.0,
        "wave_height": 3.2
    }
    
    try:
        response = requests.post(
            f"{base_url}/storm-surge/predict",
            json=prediction_data
        )
        result = response.json()
        logger.info(f"Storm surge prediction: {result}")
    except requests.exceptions.ConnectionError:
        logger.info("API not running - showing expected response format")
        logger.info("Expected response format:")
        logger.info(json.dumps({
            "is_anomaly": True,
            "threat_level": "High",
            "confidence": 0.95,
            "detector_type": "storm_surge",
            "timestamp": datetime.now().isoformat(),
            "features": prediction_data,
            "recommendations": [
                "Storm surge warning - evacuate low-lying areas",
                "High wind conditions - secure loose objects",
                "Monitor weather updates and emergency broadcasts"
            ]
        }, indent=2))


def main():
    """Run all examples."""
    logger.info("Starting Coastal Anomaly Detection Examples")
    
    # Create models directory
    import os
    os.makedirs("models", exist_ok=True)
    
    try:
        # Run examples
        example_storm_surge_detection()
        print()
        
        example_water_quality_detection()
        print()
        
        example_data_processing()
        print()
        
        example_batch_predictions()
        print()
        
        example_model_evaluation()
        print()
        
        example_api_integration()
        print()
        
        logger.info("All examples completed successfully!")
        
    except Exception as e:
        logger.error(f"Error running examples: {str(e)}")
        raise


if __name__ == "__main__":
    main()
