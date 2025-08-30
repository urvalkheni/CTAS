# 🌊 Coastal Guardian

A comprehensive AI-powered coastal monitoring and community engagement platform for protecting our coastlines through real-time threat detection and mangrove conservation.

## 🚀 Features

### 🚨 Coastal Threat Alert System
- **Real-time Monitoring**: Upload coastal data CSV or use sample data
- **AI-Powered Analysis**: Automatic threat detection for high tides, sea levels, and wave heights
- **Interactive Visualizations**: Time series charts and interactive maps
- **Alert Notifications**: Mock SMS/email alerts for community leaders

### 🌱 Community Mangrove Watch
- **Photo Upload**: Upload mangrove photos for AI analysis
- **Health Assessment**: Automated mangrove health detection (healthy vs. cut)
- **Gamification**: Points system and community leaderboard
- **Location Tracking**: Map-based reporting system

### 📈 Analytics Dashboard
- **Comprehensive Metrics**: Coastal data statistics and community impact
- **Data Export**: Download coastal data and reports as CSV
- **Trend Analysis**: Historical data visualization

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd coastal_guardian
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

```
coastal_guardian/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── data/
│   └── sample.csv        # Sample coastal monitoring data
├── reports/
│   └── contributions.json # User mangrove reports
└── utils/
    └── helpers.py        # Helper functions and utilities
```

## 🎯 Usage

### Coastal Threat Monitoring
1. Navigate to the "🚨 Threat Alerts" tab
2. Upload your coastal data CSV or use the sample data
3. View real-time metrics and threat analysis
4. Check the interactive map for alert locations

### Mangrove Conservation
1. Go to the "🌱 Mangrove Watch" tab
2. Enter your name and location
3. Upload a photo of mangrove area
4. Click "Analyze Image" for AI assessment
5. Submit your report to earn points

### Analytics
1. Visit the "📈 Analytics" tab
2. View comprehensive coastal and community metrics
3. Export data for further analysis

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **Folium**: Interactive maps
- **Ultralytics**: AI model integration (future)
- **Twilio**: SMS notifications (optional)

### AI Analysis
- **Current**: Mock analysis based on filename patterns
- **Future**: YOLOv8 integration for real mangrove detection
- **Confidence Scoring**: AI confidence levels for predictions

### Data Storage
- **Local JSON**: User contributions and reports
- **CSV Export**: Data download functionality
- **Real-time**: Live data processing and visualization

## 🎨 Features

### Theme Support
- Light theme (default)
- Dark theme
- Ocean Blue theme

### Responsive Design
- Mobile-friendly interface
- Wide layout support
- Interactive components

### Real-time Updates
- Live data visualization
- Dynamic alert system
- Community leaderboard updates

## 🚀 Future Enhancements

### AI/ML Integration
- [ ] Real YOLOv8 model for mangrove detection
- [ ] Anomaly detection for coastal threats
- [ ] Predictive analytics for tide patterns

### Communication
- [ ] Real Twilio SMS integration
- [ ] Email notification system
- [ ] Push notifications

### Data Sources
- [ ] Real-time satellite feeds
- [ ] IoT sensor integration
- [ ] Weather API integration

### Community Features
- [ ] User authentication
- [ ] Photo gallery
- [ ] Community challenges
- [ ] Reward system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built for coastal conservation and community engagement
- Inspired by the need for real-time coastal monitoring
- Powered by AI and community participation

---

**🌊 Protecting our coasts, one report at a time!**
