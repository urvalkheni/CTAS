# 🏗️ Coastal Guardian Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    COASTAL GUARDIAN PLATFORM                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │   Threat Alert  │    │  Mangrove Watch │    │  Analytics   │ │
│  │     System      │    │     System      │    │  Dashboard   │ │
│  └─────────────────┘    └─────────────────┘    └──────────────┘ │
│           │                       │                       │     │
│           ▼                       ▼                       ▼     │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    CORE PROCESSING                          │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │ │
│  │  │ Data Loader │  │ AI Analysis │  │ Visualization Engine│  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│           │                       │                       │     │
│           ▼                       ▼                       ▼     │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    DATA LAYER                               │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │ │
│  │  │ CSV Files   │  │ JSON Reports│  │ Real-time Data      │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend Layer (Streamlit)
- **Technology**: Streamlit 1.49.1
- **Features**: 
  - Responsive web interface
  - Real-time data visualization
  - Interactive maps and charts
  - File upload capabilities

### 2. Core Processing Layer

#### Data Loader (`utils/helpers.py`)
```python
def load_coastal_data(file_path=None)
def load_contributions()
def save_contribution(user, location, status, confidence)
```

#### AI Analysis Engine
```python
def analyze_threats(df)  # Coastal threat detection
def analyze_mangrove_image(filename)  # Mock AI analysis
```

#### Visualization Engine
- **Plotly**: Interactive time series charts
- **Folium**: Interactive maps with markers
- **Streamlit Components**: Metrics, tables, alerts

### 3. Data Layer

#### File Storage
- `data/sample.csv`: Sample coastal monitoring data
- `reports/contributions.json`: User mangrove reports
- Local file system for image uploads

#### Data Models

**Coastal Data Schema:**
```json
{
  "timestamp": "2024-01-01 06:00:00",
  "tide_level": 2.1,
  "sea_level": 0.8,
  "wave_height": 1.2,
  "wind_speed": 15.5,
  "location": "Mumbai"
}
```

**Contribution Schema:**
```json
{
  "user": "Rahul",
  "location": "Mumbai Coast",
  "timestamp": "2024-01-01 10:30:00",
  "points": 50,
  "status": "healthy",
  "confidence": 85
}
```

## Data Flow

### 1. Threat Alert Flow
```
CSV Upload → Data Validation → Threat Analysis → Alert Generation → Visualization
```

### 2. Mangrove Watch Flow
```
Image Upload → AI Analysis → Status Classification → Points Award → Leaderboard Update
```

### 3. Analytics Flow
```
Data Aggregation → Statistical Analysis → Metric Calculation → Export Generation
```

## Security & Performance

### Security Measures
- File type validation for uploads
- Input sanitization
- Local data storage (no external APIs)

### Performance Optimizations
- Efficient data loading with pandas
- Cached visualizations
- Responsive UI components

## Scalability Considerations

### Current Limitations
- Local file storage
- Mock AI analysis
- Single-user interface

### Future Enhancements
- Database integration (PostgreSQL/MongoDB)
- Real AI model deployment
- Multi-user authentication
- Cloud storage for images
- Real-time data streaming

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Frontend | Streamlit | 1.49.1 |
| Data Processing | Pandas | 2.3.2 |
| Visualization | Plotly | 6.3.0 |
| Maps | Folium | 0.20.0 |
| AI/ML | Mock (Future: Ultralytics) | - |
| Notifications | Mock (Future: Twilio) | - |

## Deployment Architecture

### Development
```
Local Machine → Streamlit Dev Server → Local Files
```

### Production (Future)
```
Web Server → Load Balancer → Streamlit Apps → Database → Cloud Storage
```

## Monitoring & Logging

### Current
- Console logging for errors
- Streamlit built-in monitoring

### Future
- Application performance monitoring
- Error tracking and alerting
- User analytics and metrics

---

**🌊 Built for coastal conservation and community engagement**
