const mongoose = require('mongoose');

const alertSchema = new mongoose.Schema({
  type: {
    type: String,
    enum: ['critical', 'warning', 'info'],
    required: true
  },
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    required: true
  },
  location: {
    type: String,
    required: true
  },
  coordinates: {
    latitude: Number,
    longitude: Number
  },
  severity: {
    type: String,
    enum: ['low', 'medium', 'high'],
    default: 'medium'
  },
  status: {
    type: String,
    enum: ['active', 'investigating', 'resolved', 'false_alarm'],
    default: 'active'
  },
  affectedCommunities: {
    type: Number,
    default: 0
  },
  dataSource: {
    type: String,
    required: true
  },
  confidence: {
    type: Number,
    min: 0,
    max: 100,
    default: 80
  },
  createdBy: {
    type: String,
    default: 'AI_SYSTEM'
  },
  acknowledgedBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  acknowledgedAt: Date,
  resolvedAt: Date,
  metadata: {
    sensorData: mongoose.Schema.Types.Mixed,
    satelliteData: mongoose.Schema.Types.Mixed,
    weatherData: mongoose.Schema.Types.Mixed
  }
}, {
  timestamps: true
});

// Indexes for better query performance
alertSchema.index({ type: 1, status: 1 });
alertSchema.index({ location: 1 });
alertSchema.index({ createdAt: -1 });
alertSchema.index({ coordinates: '2dsphere' });

module.exports = mongoose.model('Alert', alertSchema);
