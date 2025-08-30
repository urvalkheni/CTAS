// NOAA data slice for ocean and weather data
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunks for NOAA API calls
export const fetchCapeHenryData = createAsyncThunk(
  'noaa/fetchCapeHenryData',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('http://localhost:5001/api/noaa/cape-henry');
      
      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.message || 'Failed to fetch Cape Henry data');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchCurrentsData = createAsyncThunk(
  'noaa/fetchCurrentsData',
  async ({ stationId = 'cb0102', hours = 24 }, { rejectWithValue }) => {
    try {
      const response = await fetch(`http://localhost:5001/api/noaa/currents/${stationId}?hours=${hours}`);
      
      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.message || 'Failed to fetch currents data');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchThreatAssessment = createAsyncThunk(
  'noaa/fetchThreatAssessment',
  async ({ stationId = 'cb0102' }, { rejectWithValue }) => {
    try {
      const response = await fetch(`http://localhost:5001/api/noaa/threats/${stationId}`);
      
      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.message || 'Failed to fetch threat assessment');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const testNoaaConnection = createAsyncThunk(
  'noaa/testConnection',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('http://localhost:5001/api/noaa/test');
      
      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.message || 'NOAA connection test failed');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const initialState = {
  // Cape Henry specific data
  capeHenryData: null,
  capeHenryLastUpdated: null,
  
  // Current data
  currentData: null,
  currentLastUpdated: null,
  
  // Threat assessment
  threatAssessment: null,
  threatLastUpdated: null,
  
  // Connection status
  connectionStatus: 'disconnected', // 'connected', 'disconnected', 'testing'
  
  // Loading states
  isLoading: {
    capeHenry: false,
    currents: false,
    threats: false,
    connection: false,
  },
  
  // Errors
  errors: {
    capeHenry: null,
    currents: null,
    threats: null,
    connection: null,
  },
  
  // Data freshness (in minutes)
  dataFreshness: {
    capeHenry: null,
    currents: null,
    threats: null,
  },
};

const noaaSlice = createSlice({
  name: 'noaa',
  initialState,
  reducers: {
    clearErrors: (state) => {
      state.errors = {
        capeHenry: null,
        currents: null,
        threats: null,
        connection: null,
      };
    },
    clearCapeHenryError: (state) => {
      state.errors.capeHenry = null;
    },
    clearCurrentsError: (state) => {
      state.errors.currents = null;
    },
    clearThreatsError: (state) => {
      state.errors.threats = null;
    },
    updateDataFreshness: (state) => {
      const now = new Date();
      
      if (state.capeHenryLastUpdated) {
        state.dataFreshness.capeHenry = Math.floor(
          (now - new Date(state.capeHenryLastUpdated)) / (1000 * 60)
        );
      }
      
      if (state.currentLastUpdated) {
        state.dataFreshness.currents = Math.floor(
          (now - new Date(state.currentLastUpdated)) / (1000 * 60)
        );
      }
      
      if (state.threatLastUpdated) {
        state.dataFreshness.threats = Math.floor(
          (now - new Date(state.threatLastUpdated)) / (1000 * 60)
        );
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Cape Henry Data
      .addCase(fetchCapeHenryData.pending, (state) => {
        state.isLoading.capeHenry = true;
        state.errors.capeHenry = null;
      })
      .addCase(fetchCapeHenryData.fulfilled, (state, action) => {
        state.isLoading.capeHenry = false;
        state.capeHenryData = action.payload;
        state.capeHenryLastUpdated = new Date().toISOString();
        state.errors.capeHenry = null;
      })
      .addCase(fetchCapeHenryData.rejected, (state, action) => {
        state.isLoading.capeHenry = false;
        state.errors.capeHenry = action.payload;
      })
      
      // Currents Data
      .addCase(fetchCurrentsData.pending, (state) => {
        state.isLoading.currents = true;
        state.errors.currents = null;
      })
      .addCase(fetchCurrentsData.fulfilled, (state, action) => {
        state.isLoading.currents = false;
        state.currentData = action.payload;
        state.currentLastUpdated = new Date().toISOString();
        state.errors.currents = null;
      })
      .addCase(fetchCurrentsData.rejected, (state, action) => {
        state.isLoading.currents = false;
        state.errors.currents = action.payload;
      })
      
      // Threat Assessment
      .addCase(fetchThreatAssessment.pending, (state) => {
        state.isLoading.threats = true;
        state.errors.threats = null;
      })
      .addCase(fetchThreatAssessment.fulfilled, (state, action) => {
        state.isLoading.threats = false;
        state.threatAssessment = action.payload;
        state.threatLastUpdated = new Date().toISOString();
        state.errors.threats = null;
      })
      .addCase(fetchThreatAssessment.rejected, (state, action) => {
        state.isLoading.threats = false;
        state.errors.threats = action.payload;
      })
      
      // Connection Test
      .addCase(testNoaaConnection.pending, (state) => {
        state.isLoading.connection = true;
        state.connectionStatus = 'testing';
        state.errors.connection = null;
      })
      .addCase(testNoaaConnection.fulfilled, (state, action) => {
        state.isLoading.connection = false;
        state.connectionStatus = action.payload.success ? 'connected' : 'disconnected';
        state.errors.connection = null;
      })
      .addCase(testNoaaConnection.rejected, (state, action) => {
        state.isLoading.connection = false;
        state.connectionStatus = 'disconnected';
        state.errors.connection = action.payload;
      });
  },
});

export const { 
  clearErrors, 
  clearCapeHenryError, 
  clearCurrentsError, 
  clearThreatsError, 
  updateDataFreshness 
} = noaaSlice.actions;

export default noaaSlice.reducer;
