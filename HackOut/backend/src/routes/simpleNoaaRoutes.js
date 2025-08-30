// Simple NOAA routes for testing
const express = require('express');
const router = express.Router();

// Simple test route that doesn't call external APIs
router.get('/test', async (req, res) => {
  try {
    res.json({
      success: true,
      message: 'NOAA API routes are working',
      timestamp: new Date().toISOString(),
      apiKey: process.env.NOAA_API_KEY ? 'Present' : 'Missing'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'NOAA API test failed',
      details: error.message
    });
  }
});

// Simple echo route
router.get('/echo', (req, res) => {
  res.json({
    message: 'NOAA routes working!',
    timestamp: new Date().toISOString()
  });
});

module.exports = router;
