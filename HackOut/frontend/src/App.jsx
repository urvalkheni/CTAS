import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import LandingPage from './components/LandingPage';
import AuthSystem from './components/AuthSystem';
import InteractiveDashboardRedux from './components/InteractiveDashboardRedux';
import LogoutPage, { LogoutSuccessPage } from './components/LogoutPage';
import { useUI, useAuth } from './store/hooks';
import { setCurrentView, setAppLoading } from './store/slices/uiSlice';
import { initializeAuth } from './store/slices/authSlice';

function App() {
  const dispatch = useDispatch();
  const { currentView, loading } = useUI();
  const { user, isAuthenticated } = useAuth();

  console.log('🌊 CTAS App rendering with Redux...', { currentView, user, isAuthenticated, loading: loading.app });

  // Initialize app on load
  useEffect(() => {
    console.log('🌊 CTAS useEffect running with Redux...');
    
    const initializeApp = async () => {
      // Initialize authentication from localStorage
      console.log('🌊 About to dispatch initializeAuth...');
      dispatch(initializeAuth());
      
      // Set initial view based on auth status
      const storedUser = localStorage.getItem('ctas_user');
      const storedToken = localStorage.getItem('ctas_token');
      
      console.log('🌊 Checking auth...', { 
        storedUser: storedUser ? 'exists' : 'null', 
        storedToken: storedToken ? 'exists' : 'null',
        isAuthenticated,
        user: user?.name || 'null'
      });
      
      if (storedUser && storedToken && isAuthenticated) {
        dispatch(setCurrentView('dashboard'));
      } else {
        dispatch(setCurrentView('landing'));
      }
      
      // App initialization complete
      dispatch(setAppLoading(false));
      console.log('🌊 App loading set to false');
    };

    initializeApp();
  }, [dispatch, isAuthenticated]);

  const handleAuthSuccess = (userData) => {
    // Set session start time for logout page statistics
    localStorage.setItem('session_start', Date.now().toString());
    dispatch(setCurrentView('dashboard'));
  };

  const handleLogoutRequest = () => {
    dispatch(setCurrentView('logout'));
  };

  const handleConfirmLogout = () => {
    dispatch(setCurrentView('logout_success'));
  };

  const handleLogoutComplete = () => {
    localStorage.removeItem('ctas_user');
    localStorage.removeItem('ctas_token');
    localStorage.removeItem('session_start');
    dispatch(setCurrentView('landing'));
  };

  const handleCancelLogout = () => {
    dispatch(setCurrentView('dashboard'));
  };

  const handleGetStarted = () => {
    dispatch(setCurrentView('auth'));
  };

  const handleBackToLanding = () => {
    dispatch(setCurrentView('landing'));
  };

  // Loading screen
  // Loading screen
  if (loading.app) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center mb-4 mx-auto animate-pulse">
            <span className="text-white font-bold text-2xl">🌊</span>
          </div>
          <h2 className="text-white text-xl font-semibold mb-2">Loading CTAS</h2>
          <div className="w-32 h-2 bg-white/20 rounded-full mx-auto overflow-hidden">
            <div className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full animate-pulse"></div>
          </div>
        </div>
      </div>
    );
  }

  // Route based on current view
  switch (currentView) {
    case 'auth':
      return (
        <AuthSystem 
          onAuthSuccess={handleAuthSuccess}
          onBack={handleBackToLanding}
        />
      );
    
    case 'dashboard':
      return (
        <InteractiveDashboardRedux 
          user={user}
          onLogout={handleLogoutRequest}
        />
      );
    
    case 'logout':
      return (
        <LogoutPage
          user={user}
          onConfirmLogout={handleConfirmLogout}
          onCancel={handleCancelLogout}
        />
      );
    
    case 'logout_success':
      return (
        <LogoutSuccessPage
          onReturnHome={handleLogoutComplete}
        />
      );
    
    case 'landing':
    default:
      return (
        <LandingPage 
          onGetStarted={handleGetStarted}
        />
      );
  }
}

export default App;
