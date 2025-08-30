"""
FastAPI Application for Coastal Anomaly Detection

This module provides a REST API for the coastal anomaly detection system,
allowing real-time predictions and model management.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import os
import json

from .models import CoastalAnomalyDetector, StormSurgeDetector, WaterQualityDetector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Coastal Guardian - Anomaly Detection API",
    description="AI/ML API for detecting coastal anomalies including storm surges, rising sea levels, and illegal dumping",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instances
storm_surge_detector = StormSurgeDetector()
water_quality_detector = WaterQualityDetector()
general_detector = CoastalAnomalyDetector()

# Model storage directory
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)


# Pydantic models for request/response
class PredictionRequest(BaseModel):
    """Request model for single prediction."""
    sea_level: Optional[float] = Field(None, description="Sea level in meters")
    wind_speed: Optional[float] = Field(None, description="Wind speed in m/s")
    atmospheric_pressure: Optional[float] = Field(None, description="Atmospheric pressure in hPa")
    wave_height: Optional[float] = Field(None, description="Wave height in meters")
    ph: Optional[float] = Field(None, description="Water pH level")
    turbidity: Optional[float] = Field(None, description="Water turbidity in NTU")
    dissolved_oxygen: Optional[float] = Field(None, description="Dissolved oxygen in mg/L")
    temperature: Optional[float] = Field(None, description="Water temperature in Celsius")
    conductivity: Optional[float] = Field(None, description="Water conductivity in mS/cm")


class PredictionResponse(BaseModel):
    """Response model for predictions."""
    is_anomaly: bool
    threat_level: str
    confidence: float
    detector_type: str
    timestamp: datetime
    features: Dict[str, float]
    recommendations: List[str]


class BatchPredictionRequest(BaseModel):
    """Request model for batch predictions."""
    data: List[Dict[str, float]]
    detector_type: str = "general"


class ModelInfo(BaseModel):
    """Model information response."""
    model_type: str
    is_trained: bool
    feature_columns: List[str]
    contamination: float
    last_trained: Optional[datetime]


class TrainingRequest(BaseModel):
    """Request model for training."""
    data_url: str
    feature_columns: List[str]
    model_type: str = "isolation_forest"
    contamination: float = 0.05


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Coastal Guardian Anomaly Detection API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "batch_predict": "/batch-predict",
            "model_info": "/model-info/{detector_type}",
            "train": "/train",
            "storm_surge_predict": "/storm-surge/predict",
            "water_quality_predict": "/water-quality/predict"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "models": {
            "storm_surge": storm_surge_detector.is_trained,
            "water_quality": water_quality_detector.is_trained,
            "general": general_detector.is_trained
        }
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_anomaly(request: PredictionRequest):
    """
    Predict anomaly for a single data point using the general detector.
    
    This endpoint accepts various coastal monitoring parameters and returns
    anomaly detection results with threat assessment.
    """
    try:
        # Convert request to dictionary, removing None values
        features = {k: v for k, v in request.dict().items() if v is not None}
        
        if not features:
            raise HTTPException(status_code=400, detail="At least one feature must be provided")
        
        # Make prediction
        result = general_detector.predict_single(**features)
        
        # Generate recommendations based on anomaly type
        recommendations = []
        if result["is_anomaly"]:
            if "sea_level" in features and features["sea_level"] > 2.0:
                recommendations.append("High sea level detected - monitor for storm surge")
            if "wind_speed" in features and features["wind_speed"] > 20.0:
                recommendations.append("High wind speed detected - potential storm conditions")
            if "ph" in features and (features["ph"] < 6.5 or features["ph"] > 8.5):
                recommendations.append("Abnormal pH levels - check for pollution sources")
        
        return PredictionResponse(
            is_anomaly=result["is_anomaly"],
            threat_level=result["threat_level"],
            confidence=result["confidence"],
            detector_type="general",
            timestamp=datetime.now(),
            features=features,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/storm-surge/predict", response_model=PredictionResponse)
async def predict_storm_surge(request: PredictionRequest):
    """
    Predict storm surge anomalies using specialized storm surge detector.
    """
    try:
        # Extract storm surge relevant features
        features = {}
        if request.sea_level is not None:
            features["sea_level"] = request.sea_level
        if request.wind_speed is not None:
            features["wind_speed"] = request.wind_speed
        if request.atmospheric_pressure is not None:
            features["atmospheric_pressure"] = request.atmospheric_pressure
        if request.wave_height is not None:
            features["wave_height"] = request.wave_height
        
        if not features:
            raise HTTPException(status_code=400, detail="At least one storm surge feature must be provided")
        
        # Make prediction
        result = storm_surge_detector.predict_single(**features)
        
        # Generate storm surge specific recommendations
        recommendations = []
        if result["is_anomaly"]:
            if "sea_level" in features and features["sea_level"] > 1.5:
                recommendations.append("Storm surge warning - evacuate low-lying areas")
            if "wind_speed" in features and features["wind_speed"] > 25.0:
                recommendations.append("High wind conditions - secure loose objects")
            recommendations.append("Monitor weather updates and emergency broadcasts")
        
        return PredictionResponse(
            is_anomaly=result["is_anomaly"],
            threat_level=result["threat_level"],
            confidence=result["confidence"],
            detector_type="storm_surge",
            timestamp=datetime.now(),
            features=features,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Storm surge prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Storm surge prediction failed: {str(e)}")


@app.post("/water-quality/predict", response_model=PredictionResponse)
async def predict_water_quality(request: PredictionRequest):
    """
    Predict water quality anomalies (illegal dumping detection).
    """
    try:
        # Extract water quality relevant features
        features = {}
        if request.ph is not None:
            features["ph"] = request.ph
        if request.turbidity is not None:
            features["turbidity"] = request.turbidity
        if request.dissolved_oxygen is not None:
            features["dissolved_oxygen"] = request.dissolved_oxygen
        if request.temperature is not None:
            features["temperature"] = request.temperature
        if request.conductivity is not None:
            features["conductivity"] = request.conductivity
        
        if not features:
            raise HTTPException(status_code=400, detail="At least one water quality feature must be provided")
        
        # Make prediction
        result = water_quality_detector.predict_single(**features)
        
        # Generate water quality specific recommendations
        recommendations = []
        if result["is_anomaly"]:
            if "ph" in features and (features["ph"] < 6.0 or features["ph"] > 9.0):
                recommendations.append("Critical pH levels - investigate pollution sources")
            if "turbidity" in features and features["turbidity"] > 10.0:
                recommendations.append("High turbidity detected - possible sediment runoff")
            if "dissolved_oxygen" in features and features["dissolved_oxygen"] < 4.0:
                recommendations.append("Low oxygen levels - potential fish kill risk")
            recommendations.append("Collect water samples for laboratory analysis")
            recommendations.append("Check for nearby industrial discharges")
        
        return PredictionResponse(
            is_anomaly=result["is_anomaly"],
            threat_level=result["threat_level"],
            confidence=result["confidence"],
            detector_type="water_quality",
            timestamp=datetime.now(),
            features=features,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Water quality prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Water quality prediction failed: {str(e)}")


@app.post("/batch-predict")
async def batch_predict(request: BatchPredictionRequest):
    """
    Predict anomalies for multiple data points.
    """
    try:
        if not request.data:
            raise HTTPException(status_code=400, detail="No data provided")
        
        # Convert to DataFrame
        df = pd.DataFrame(request.data)
        
        # Select appropriate detector
        if request.detector_type == "storm_surge":
            detector = storm_surge_detector
        elif request.detector_type == "water_quality":
            detector = water_quality_detector
        else:
            detector = general_detector
        
        # Make predictions
        predictions = detector.predict(df)
        
        # Format results
        results = []
        for i, pred in enumerate(predictions):
            results.append({
                "index": i,
                "is_anomaly": pred == -1,
                "threat_level": "High" if pred == -1 else "Low",
                "features": request.data[i]
            })
        
        return {
            "predictions": results,
            "total_predictions": len(results),
            "anomalies_detected": sum(1 for r in results if r["is_anomaly"]),
            "detector_type": request.detector_type,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")


@app.get("/model-info/{detector_type}", response_model=ModelInfo)
async def get_model_info(detector_type: str):
    """
    Get information about a specific model.
    """
    try:
        if detector_type == "storm_surge":
            detector = storm_surge_detector
        elif detector_type == "water_quality":
            detector = water_quality_detector
        elif detector_type == "general":
            detector = general_detector
        else:
            raise HTTPException(status_code=400, detail="Invalid detector type")
        
        return ModelInfo(
            model_type=detector.model_type,
            is_trained=detector.is_trained,
            feature_columns=detector.feature_columns,
            contamination=detector.contamination,
            last_trained=None  # Could be added to the model class
        )
        
    except Exception as e:
        logger.error(f"Model info error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")


@app.post("/train")
async def train_model(request: TrainingRequest, background_tasks: BackgroundTasks):
    """
    Train a model with provided data.
    """
    try:
        # Load data from URL (could be file path or URL)
        if request.data_url.endswith('.csv'):
            df = pd.read_csv(request.data_url)
        else:
            raise HTTPException(status_code=400, detail="Unsupported data format")
        
        # Select appropriate detector based on features
        if any(feature in request.feature_columns for feature in ["sea_level", "wind_speed", "atmospheric_pressure"]):
            detector = storm_surge_detector
            detector_type = "storm_surge"
        elif any(feature in request.feature_columns for feature in ["ph", "turbidity", "dissolved_oxygen"]):
            detector = water_quality_detector
            detector_type = "water_quality"
        else:
            detector = general_detector
            detector_type = "general"
        
        # Train model
        detector.train(df, request.feature_columns, contamination=request.contamination)
        
        # Save model
        model_path = os.path.join(MODEL_DIR, f"{detector_type}_model.pkl")
        detector.save_model(model_path)
        
        return {
            "message": f"{detector_type} model trained successfully",
            "model_path": model_path,
            "features_used": request.feature_columns,
            "data_points": len(df),
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Training error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@app.get("/models")
async def list_models():
    """
    List all available trained models.
    """
    try:
        models = []
        for filename in os.listdir(MODEL_DIR):
            if filename.endswith('.pkl'):
                model_path = os.path.join(MODEL_DIR, filename)
                model_info = {
                    "name": filename,
                    "path": model_path,
                    "size": os.path.getsize(model_path),
                    "modified": datetime.fromtimestamp(os.path.getmtime(model_path))
                }
                models.append(model_info)
        
        return {
            "models": models,
            "total_models": len(models)
        }
        
    except Exception as e:
        logger.error(f"List models error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list models: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
