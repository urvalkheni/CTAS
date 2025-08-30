// Redux store configuration for CTAS
import { configureStore } from '@reduxjs/toolkit';
import authSlice from './slices/authSlice';
import noaaSlice from './slices/noaaSlice';
import alertSlice from './slices/alertSlice';
import uiSlice from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    auth: authSlice,
    noaa: noaaSlice,
    alerts: alertSlice,
    ui: uiSlice,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
});
