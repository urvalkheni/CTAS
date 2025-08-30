// Dashboard data provider for real-time updates
import React, { useEffect, useRef } from 'react';
import { useDispatch } from 'react-redux';
import { useNoaaData, useUI, useAlerts } from '../store/hooks';
import { 
  fetchCapeHenryData, 
  fetchCurrentsData, 
  fetchThreatAssessment,
  testNoaaConnection,
  updateDataFreshness 
} from '../store/slices/noaaSlice';
import { 
  fetchAlerts,
  processNoaaData,
  addLocalAlert 
} from '../store/slices/alertSlice';
import { setSyncStatus, setOnlineStatus } from '../store/slices/uiSlice';

const DashboardProvider = ({ children }) => {
  const dispatch = useDispatch();
  const refreshIntervalRef = useRef(null);
  const freshnessIntervalRef = useRef(null);
  const connectionCheckRef = useRef(null);
  
  const { connectionStatus, dataFreshness } = useNoaaData();
  const { dashboard } = useUI();
  const { autoAlerts } = useAlerts();

  // Initialize dashboard data
  useEffect(() => {
    const initializeDashboard = async () => {
      dispatch(setSyncStatus('syncing'));
      
      try {
        // Test NOAA connection
        await dispatch(testNoaaConnection()).unwrap();
        
        // Fetch initial data
        await Promise.all([
          dispatch(fetchCapeHenryData()),
          dispatch(fetchCurrentsData({ stationId: 'cb0102' })),
          dispatch(fetchThreatAssessment({ stationId: 'cb0102' })),
          dispatch(fetchAlerts()),
        ]);
        
        dispatch(setSyncStatus('idle'));
      } catch (error) {
        console.error('Dashboard initialization failed:', error);
        dispatch(setSyncStatus('error'));
      }
    };

    initializeDashboard();
  }, [dispatch]);

  // Auto-refresh data based on user preferences
  useEffect(() => {
    if (dashboard.autoRefresh && dashboard.refreshInterval && connectionStatus === 'connected') {
      refreshIntervalRef.current = setInterval(() => {
        dispatch(setSyncStatus('syncing'));
        
        Promise.all([
          dispatch(fetchCapeHenryData()),
          dispatch(fetchCurrentsData({ stationId: 'cb0102' })),
          dispatch(fetchThreatAssessment({ stationId: 'cb0102' })),
        ]).then(() => {
          dispatch(setSyncStatus('idle'));
        }).catch(() => {
          dispatch(setSyncStatus('error'));
        });
      }, dashboard.refreshInterval);
    }

    return () => {
      if (refreshIntervalRef.current) {
        clearInterval(refreshIntervalRef.current);
      }
    };
  }, [dispatch, dashboard.autoRefresh, dashboard.refreshInterval, connectionStatus]);

  // Update data freshness every minute
  useEffect(() => {
    freshnessIntervalRef.current = setInterval(() => {
      dispatch(updateDataFreshness());
    }, 60000); // Update every minute

    return () => {
      if (freshnessIntervalRef.current) {
        clearInterval(freshnessIntervalRef.current);
      }
    };
  }, [dispatch]);

  // Periodic connection check
  useEffect(() => {
    connectionCheckRef.current = setInterval(() => {
      dispatch(testNoaaConnection());
    }, 5 * 60 * 1000); // Check every 5 minutes

    return () => {
      if (connectionCheckRef.current) {
        clearInterval(connectionCheckRef.current);
      }
    };
  }, [dispatch]);

  // Monitor online status
  useEffect(() => {
    const handleOnline = () => {
      dispatch(setOnlineStatus(true));
      
      // Reconnect and refresh data when coming back online
      if (connectionStatus === 'disconnected') {
        dispatch(testNoaaConnection()).then(() => {
          dispatch(fetchCapeHenryData());
          dispatch(fetchCurrentsData({ stationId: 'cb0102' }));
        });
      }
    };

    const handleOffline = () => {
      dispatch(setOnlineStatus(false));
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [dispatch, connectionStatus]);

  // Monitor data freshness and create alerts
  useEffect(() => {
    if (autoAlerts.dataOutage) {
      const checkDataFreshness = () => {
        Object.entries(dataFreshness).forEach(([dataType, minutes]) => {
          if (minutes > 60) { // More than 1 hour old
            dispatch(addLocalAlert({
              type: 'data_outage',
              severity: minutes > 180 ? 'high' : 'medium',
              title: 'Data Outage Detected',
              message: `${dataType} data is ${minutes} minutes old`,
              data: { dataType, minutes },
            }));
          }
        });
      };

      const freshnessCheckInterval = setInterval(checkDataFreshness, 10 * 60 * 1000); // Check every 10 minutes

      return () => clearInterval(freshnessCheckInterval);
    }
  }, [dispatch, dataFreshness, autoAlerts.dataOutage]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (refreshIntervalRef.current) clearInterval(refreshIntervalRef.current);
      if (freshnessIntervalRef.current) clearInterval(freshnessIntervalRef.current);
      if (connectionCheckRef.current) clearInterval(connectionCheckRef.current);
    };
  }, []);

  return <>{children}</>;
};

export default DashboardProvider;
