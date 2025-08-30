const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const path = require('path');
const connectDB = require('./lib/db.js')


require('dotenv').config({ path: path.join(__dirname, '../../.env') });


const app = express();
const PORT = process.env.PORT || 5000;

// Connect to Database (commented out for now - requires MongoDB)
// connectDB();

// Security Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  credentials: true
}));

// Rate Limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});
app.use('/api/', limiter);

// Body Parsing Middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Compression
app.use(compression());

// Logging
app.use(morgan('combined'));

// Health Check Route
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'OK',
    message: 'CTAS Backend Server is running',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    environment: process.env.NODE_ENV || 'development'
  });
});

// API Routes
app.use('/api/auth', require('./routes/auth'));
app.use('/api/threats', require('./routes/threats'));
app.use('/api/reports', require('./routes/reports'));
app.use('/api/weather', require('./routes/weather'));
app.use('/api/satellite', require('./routes/satellite'));
app.use('/api/users', require('./routes/users'));
app.use('/api/noaa', require('./routes/simpleNoaaRoutes'));
app.use('/api/community-reports', require('./routes/communityReports'));

// Test Weather Service Route
app.get('/api/test/weather', async (req, res) => {
  try {
    const OpenWeatherMapService = require('./services/openWeatherMapService');
    const weatherService = new OpenWeatherMapService(process.env.OPENWEATHER_API_KEY);
    
    const testResult = await weatherService.testAPIKey();
    
    if (testResult.status === 'success') {
      const currentWeather = await weatherService.getCurrentWeather('Mumbai');
      res.json({
        status: 'success',
        message: 'Weather service is working',
        apiKeyValid: true,
        sampleData: currentWeather
      });
    } else {
      res.status(400).json({
        status: 'error',
        message: 'Weather API key not working',
        error: testResult.message
      });
    }
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: 'Weather service error',
      error: error.message
    });
  }
});

// Catch all handler
app.get('*', (req, res) => {
  res.status(404).json({
    status: 'error',
    message: 'Route not found',
    path: req.originalUrl
  });
});

// Global Error Handler
app.use((err, req, res, next) => {
  console.error('Error:', err.stack);
  
  res.status(err.status || 500).json({
    status: 'error',
    message: err.message || 'Internal Server Error',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
});

// Graceful Shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received. Shutting down gracefully...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received. Shutting down gracefully...');
  process.exit(0);
});

app.listen(PORT, () => {
  connectDB();
  console.log(`
🌊 CTAS Backend Server Starting...
==========================================
📍 Server: http://localhost:${PORT}
🌐 Environment: ${process.env.NODE_ENV || 'development'}
🔑 API Key: ${process.env.OPENWEATHER_API_KEY ? 'Configured' : 'Missing'}
⏰ Started: ${new Date().toISOString()}
==========================================
🚀 Server is ready for connections!
  `);
});

module.exports = app;
