import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true
  },
  password: {
    type: String,
    required: true
  },
  location: {
    type: String,
    trim: true
  },
  avatar: {
    type: String
  },
  points: {
    type: Number,
    default: 0
  },
  reportsCount: {
    type: Number,
    default: 0
  },
  role: {
    type: String,
    enum: ['user', 'admin', 'moderator'],
    default: 'user'
  },
  isPublic: {
    type: Boolean,
    default: true
  },
  showOnLeaderboard: {
    type: Boolean,
    default: true
  },
  notifications: {
    email: {
      type: Boolean,
      default: true
    },
    sms: {
      type: Boolean,
      default: false
    },
    highPriority: {
      type: Boolean,
      default: true
    }
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

// Update the updatedAt field before saving
userSchema.pre('save', function(next) {
  this.updatedAt = new Date();
  next();
});

export default mongoose.models.User || mongoose.model('User', userSchema);
