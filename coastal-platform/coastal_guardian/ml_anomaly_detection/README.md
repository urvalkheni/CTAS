# Coastal Guardian - ML Anomaly Detection System

## Overview

The ML Anomaly Detection System is a comprehensive AI/ML solution for detecting anomalies in coastal monitoring data. It provides specialized detection capabilities for:

- **Storm Surge Detection**: Monitors sea level, wind speed, atmospheric pressure, and wave height
- **Water Quality Monitoring**: Detects illegal dumping and pollution through pH, turbidity, dissolved oxygen, temperature, and conductivity monitoring
- **General Anomaly Detection**: Flexible system for various coastal monitoring parameters

## Features

### 🚨 Anomaly Detection
- **Isolation Forest**: Primary algorithm for detecting outliers in coastal data
- **LSTM Support**: Framework for time-series anomaly detection (extensible)
- **Multiple Detector Types**: Specialized detectors for different anomaly types
- **Real-time Processing**: Fast prediction capabilities for live data streams

### 📊 Data Processing
- **Comprehensive Cleaning**: Handles missing values, outliers, and data quality issues
- **Feature Engineering**: Creates time-based features, rolling statistics, and interaction terms
- **Multiple Scaling Methods**: Standard, MinMax, and Robust scaling options
- **Validation**: Input data validation and quality checks

### 🌐 API Integration
- **FastAPI REST API**: Modern, fast web framework for exposing detection results
- **Multiple Endpoints**: Specialized endpoints for different anomaly types
- **Batch Processing**: Support for processing multiple data points at once
- **Model Management**: Train, save, and load models via API

### 🛠️ Utilities
- **Sample Data Generation**: Generate realistic test data for development and testing
- **Model Evaluation**: Comprehensive performance metrics and evaluation tools
- **Alert Generation**: Human-readable alert messages with recommendations
- **Configuration Management**: Easy pipeline configuration for different data types

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd coastal-platform/coastal_guardian/ml_anomaly_detection
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify installation**:
```bash
python -c "import pandas, sklearn, fastapi; print('Installation successful!')"
```

## Quick Start

### 1. Basic Usage

```python
from models import StormSurgeDetector
from utils import generate_sample_data

# Generate sample data
data = generate_sample_data(n_samples=1000, data_type="storm_surge")

# Initialize and train detector
detector = StormSurgeDetector()
detector.train(data, ['sea_level', 'wind_speed', 'atmospheric_pressure', 'wave_height'])

# Make prediction
result = detector.predict_single(
    sea_level=3.5,
    wind_speed=45.0,
    atmospheric_pressure=985.0,
    wave_height=4.2
)

print(f"Anomaly detected: {result['is_anomaly']}")
print(f"Threat level: {result['threat_level']}")
```

### 2. API Usage

Start the API server:
```bash
python api.py
```

Make predictions via HTTP:
```bash
curl -X POST "http://localhost:8000/storm-surge/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "sea_level": 3.5,
       "wind_speed": 45.0,
       "atmospheric_pressure": 985.0,
       "wave_height": 4.2
     }'
```

### 3. Run Examples

```bash
python example_usage.py
```

## API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and available endpoints |
| `/health` | GET | Health check and model status |
| `/predict` | POST | General anomaly detection |
| `/batch-predict` | POST | Batch anomaly detection |
| `/model-info/{detector_type}` | GET | Model information |

### Specialized Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/storm-surge/predict` | POST | Storm surge specific detection |
| `/water-quality/predict` | POST | Water quality anomaly detection |
| `/train` | POST | Train new models |
| `/models` | GET | List available models |

### Example API Response

```json
{
  "is_anomaly": true,
  "threat_level": "High",
  "confidence": 0.95,
  "detector_type": "storm_surge",
  "timestamp": "2024-01-15T10:30:00",
  "features": {
    "sea_level": 3.5,
    "wind_speed": 45.0,
    "atmospheric_pressure": 985.0,
    "wave_height": 4.2
  },
  "recommendations": [
    "Storm surge warning - evacuate low-lying areas",
    "High wind conditions - secure loose objects",
    "Monitor weather updates and emergency broadcasts"
  ]
}
```

## Data Types

### Storm Surge Data
- **sea_level**: Sea level in meters
- **wind_speed**: Wind speed in m/s
- **atmospheric_pressure**: Atmospheric pressure in hPa
- **wave_height**: Wave height in meters

### Water Quality Data
- **ph**: Water pH level (0-14)
- **turbidity**: Water turbidity in NTU
- **dissolved_oxygen**: Dissolved oxygen in mg/L
- **temperature**: Water temperature in Celsius
- **conductivity**: Water conductivity in mS/cm

## Model Types

### 1. CoastalAnomalyDetector
General-purpose anomaly detector supporting multiple algorithms:
- Isolation Forest (default)
- LSTM (framework ready)

### 2. StormSurgeDetector
Specialized detector for storm surge conditions:
- Optimized for weather data
- Robust scaling for outlier resistance
- Storm-specific feature engineering

### 3. WaterQualityDetector
Specialized detector for water quality anomalies:
- Pollution detection
- Illegal dumping identification
- Water quality index calculation

## Data Processing Pipeline

### 1. Data Cleaning
- Remove duplicates
- Handle missing values (forward/backward fill, KNN imputation)
- Remove outliers (IQR method, Z-score)
- Validate data types

### 2. Feature Engineering
- Time-based features (hour, day, month, year, day of week)
- Rolling statistics (mean, standard deviation)
- Lag features (previous values)
- Difference features (rate of change)
- Interaction features (feature combinations)
- Environmental indices

### 3. Normalization
- Standard scaling (default)
- MinMax scaling
- Robust scaling (for weather data)

## Configuration

### Training Pipeline Configuration

```python
from utils import create_training_pipeline

# Storm surge configuration
config = create_training_pipeline("storm_surge")
# Returns:
# {
#     'model_type': 'isolation_forest',
#     'contamination': 0.03,
#     'feature_columns': ['sea_level', 'wind_speed', 'atmospheric_pressure', 'wave_height'],
#     'scaling_method': 'robust',
#     'outlier_method': 'iqr'
# }
```

### Model Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `contamination` | Expected proportion of anomalies | 0.05 | 0.01-0.1 |
| `model_type` | Algorithm type | "isolation_forest" | "isolation_forest", "lstm" |
| `scaling_method` | Data scaling method | "standard" | "standard", "minmax", "robust" |

## Performance Metrics

The system provides comprehensive evaluation metrics:

- **Precision**: Accuracy of anomaly predictions
- **Recall**: Ability to detect all anomalies
- **F1-Score**: Harmonic mean of precision and recall
- **Accuracy**: Overall prediction accuracy
- **Anomaly Detection Rate**: Proportion of data flagged as anomalies
- **True Anomaly Rate**: Actual proportion of anomalies in data

## Alert System

### Alert Types

1. **Storm Surge Alerts**
   - High sea level warnings
   - Wind speed alerts
   - Evacuation recommendations

2. **Water Quality Alerts**
   - pH level warnings
   - Pollution detection
   - Sample collection recommendations

3. **General Anomaly Alerts**
   - Custom alert messages
   - Severity classification
   - Action recommendations

### Alert Format

```
🚨 STORM SURGE ALERT - HIGH 🚨
Time: 2024-01-15 10:30:00

Sea Level: 3.5 meters
Wind Speed: 45.0 m/s
Atmospheric Pressure: 985.0 hPa
Wave Height: 4.2 meters

RECOMMENDATIONS:
- Monitor weather updates
- Secure loose objects
- Evacuate low-lying areas if necessary
- Follow emergency protocols
```

## Development

### Project Structure

```
ml_anomaly_detection/
├── __init__.py              # Package initialization
├── models.py               # ML models and detectors
├── api.py                  # FastAPI application
├── data_processor.py       # Data processing pipeline
├── utils.py                # Utility functions
├── example_usage.py        # Usage examples
├── requirements.txt        # Dependencies
└── README.md              # This file
```

### Adding New Detectors

1. **Create detector class**:
```python
class CustomDetector(CoastalAnomalyDetector):
    def __init__(self):
        super().__init__(model_type="isolation_forest", contamination=0.05)
        self.default_features = ["feature1", "feature2"]
    
    def train(self, df, feature_columns=None):
        if feature_columns is None:
            feature_columns = [col for col in self.default_features if col in df.columns]
        super().train(df, feature_columns)
```

2. **Add API endpoint**:
```python
@app.post("/custom/predict", response_model=PredictionResponse)
async def predict_custom(request: PredictionRequest):
    # Implementation here
    pass
```

### Testing

Run the test suite:
```bash
pytest tests/
```

Run examples:
```bash
python example_usage.py
```

## Deployment

### Production Considerations

1. **Model Persistence**: Save trained models to disk
2. **API Security**: Implement authentication and rate limiting
3. **Monitoring**: Add logging and performance monitoring
4. **Scalability**: Consider containerization with Docker
5. **Data Validation**: Implement strict input validation

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is part of the Coastal Guardian platform and follows the same licensing terms.

## Support

For questions and support:
- Check the examples in `example_usage.py`
- Review the API documentation at `http://localhost:8000/docs`
- Open an issue in the repository

## Roadmap

- [ ] Advanced LSTM implementation
- [ ] Real-time streaming support
- [ ] Additional anomaly detection algorithms
- [ ] Web dashboard for monitoring
- [ ] Integration with external data sources
- [ ] Mobile app support
