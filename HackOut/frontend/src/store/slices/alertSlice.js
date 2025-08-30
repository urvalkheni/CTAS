// Alerts slice for threat notifications and user alerts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunks for alerts API calls
export const fetchAlerts = createAsyncThunk(
  'alerts/fetchAlerts',
  async (_, { rejectWithValue, getState }) => {
    try {
      const { auth } = getState();
      const response = await fetch('http://localhost:5001/api/alerts', {
        headers: {
          'Authorization': `Bearer ${auth.token}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.message || 'Failed to fetch alerts');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const createAlert = createAsyncThunk(
  'alerts/createAlert',
  async (alertData, { rejectWithValue, getState }) => {
    try {
      const { auth } = getState();
      const response = await fetch('http://localhost:5001/api/alerts', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${auth.token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(alertData),
      });
      
      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.message || 'Failed to create alert');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const markAlertAsRead = createAsyncThunk(
  'alerts/markAsRead',
  async (alertId, { rejectWithValue, getState }) => {
    try {
      const { auth } = getState();
      const response = await fetch(`http://localhost:5001/api/alerts/${alertId}/read`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${auth.token}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.message || 'Failed to mark alert as read');
      }
      
      const data = await response.json();
      return { alertId, ...data };
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const deleteAlert = createAsyncThunk(
  'alerts/deleteAlert',
  async (alertId, { rejectWithValue, getState }) => {
    try {
      const { auth } = getState();
      const response = await fetch(`http://localhost:5001/api/alerts/${alertId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${auth.token}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.message || 'Failed to delete alert');
      }
      
      return alertId;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const initialState = {
  alerts: [],
  unreadCount: 0,
  isLoading: false,
  error: null,
  lastFetch: null,
  
  // Alert filters
  filters: {
    severity: 'all', // 'all', 'low', 'medium', 'high', 'critical'
    type: 'all', // 'all', 'current', 'weather', 'threat', 'system'
    status: 'all', // 'all', 'unread', 'read'
  },
  
  // Real-time notifications
  notifications: {
    enabled: true,
    sound: true,
    desktop: false,
  },
  
  // Auto-generated alerts from NOAA data
  autoAlerts: {
    highCurrents: true,
    severeWeather: true,
    rapidChanges: true,
    dataOutage: true,
  },
};

const alertsSlice = createSlice({
  name: 'alerts',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    
    setFilter: (state, action) => {
      const { filterType, value } = action.payload;
      state.filters[filterType] = value;
    },
    
    toggleNotification: (state, action) => {
      const { notificationType } = action.payload;
      state.notifications[notificationType] = !state.notifications[notificationType];
    },
    
    toggleAutoAlert: (state, action) => {
      const { alertType } = action.payload;
      state.autoAlerts[alertType] = !state.autoAlerts[alertType];
    },
    
    addLocalAlert: (state, action) => {
      // For real-time alerts that don't need server persistence
      const alert = {
        id: `local_${Date.now()}`,
        ...action.payload,
        isLocal: true,
        timestamp: new Date().toISOString(),
        read: false,
      };
      state.alerts.unshift(alert);
      state.unreadCount += 1;
    },
    
    markLocalAlertAsRead: (state, action) => {
      const { alertId } = action.payload;
      const alert = state.alerts.find(a => a.id === alertId);
      if (alert && !alert.read) {
        alert.read = true;
        state.unreadCount = Math.max(0, state.unreadCount - 1);
      }
    },
    
    removeLocalAlert: (state, action) => {
      const { alertId } = action.payload;
      const index = state.alerts.findIndex(a => a.id === alertId);
      if (index !== -1) {
        const alert = state.alerts[index];
        if (!alert.read) {
          state.unreadCount = Math.max(0, state.unreadCount - 1);
        }
        state.alerts.splice(index, 1);
      }
    },
    
    updateUnreadCount: (state) => {
      state.unreadCount = state.alerts.filter(alert => !alert.read).length;
    },
    
    // Process NOAA data for auto-alerts
    processNoaaData: (state, action) => {
      const { noaaData } = action.payload;
      
      if (!noaaData) return;
      
      // Check for high current conditions
      if (state.autoAlerts.highCurrents && noaaData.currentData) {
        const currentSpeed = noaaData.currentData.latest?.speed;
        if (currentSpeed && currentSpeed > 3.0) { // 3+ knots considered high
          const existingAlert = state.alerts.find(
            a => a.type === 'high_currents' && a.isLocal && !a.resolved
          );
          
          if (!existingAlert) {
            const alert = {
              id: `local_high_currents_${Date.now()}`,
              type: 'high_currents',
              severity: currentSpeed > 5.0 ? 'high' : 'medium',
              title: 'High Current Conditions Detected',
              message: `Current speed is ${currentSpeed.toFixed(1)} knots at Cape Henry`,
              timestamp: new Date().toISOString(),
              read: false,
              isLocal: true,
              data: { currentSpeed, location: 'Cape Henry' },
            };
            state.alerts.unshift(alert);
            state.unreadCount += 1;
          }
        }
      }
      
      // Check for rapid changes
      if (state.autoAlerts.rapidChanges && noaaData.threatAssessment) {
        const threatLevel = noaaData.threatAssessment.overall;
        if (threatLevel === 'HIGH' || threatLevel === 'CRITICAL') {
          const existingAlert = state.alerts.find(
            a => a.type === 'threat_level' && a.isLocal && !a.resolved
          );
          
          if (!existingAlert) {
            const alert = {
              id: `local_threat_${Date.now()}`,
              type: 'threat_level',
              severity: threatLevel === 'CRITICAL' ? 'critical' : 'high',
              title: `${threatLevel} Threat Level Detected`,
              message: `Current threat assessment shows ${threatLevel} risk conditions`,
              timestamp: new Date().toISOString(),
              read: false,
              isLocal: true,
              data: { threatLevel, assessment: noaaData.threatAssessment },
            };
            state.alerts.unshift(alert);
            state.unreadCount += 1;
          }
        }
      }
    },
  },
  
  extraReducers: (builder) => {
    builder
      // Fetch Alerts
      .addCase(fetchAlerts.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchAlerts.fulfilled, (state, action) => {
        state.isLoading = false;
        state.alerts = action.payload.alerts || [];
        state.unreadCount = state.alerts.filter(alert => !alert.read).length;
        state.lastFetch = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchAlerts.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Create Alert
      .addCase(createAlert.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createAlert.fulfilled, (state, action) => {
        state.isLoading = false;
        state.alerts.unshift(action.payload);
        if (!action.payload.read) {
          state.unreadCount += 1;
        }
        state.error = null;
      })
      .addCase(createAlert.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Mark as Read
      .addCase(markAlertAsRead.fulfilled, (state, action) => {
        const { alertId } = action.payload;
        const alert = state.alerts.find(a => a.id === alertId);
        if (alert && !alert.read) {
          alert.read = true;
          state.unreadCount = Math.max(0, state.unreadCount - 1);
        }
      })
      
      // Delete Alert
      .addCase(deleteAlert.fulfilled, (state, action) => {
        const alertId = action.payload;
        const index = state.alerts.findIndex(a => a.id === alertId);
        if (index !== -1) {
          const alert = state.alerts[index];
          if (!alert.read) {
            state.unreadCount = Math.max(0, state.unreadCount - 1);
          }
          state.alerts.splice(index, 1);
        }
      });
  },
});

export const {
  clearError,
  setFilter,
  toggleNotification,
  toggleAutoAlert,
  addLocalAlert,
  markLocalAlertAsRead,
  removeLocalAlert,
  updateUnreadCount,
  processNoaaData,
} = alertsSlice.actions;

export default alertsSlice.reducer;
