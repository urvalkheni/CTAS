// Enhanced Error Boundary for CTAS Application
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
    
    // Log the error
    console.error('CTAS Error Boundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-red-900 to-slate-800 flex items-center justify-center p-4">
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-8 max-w-2xl w-full">
            <div className="text-center mb-6">
              <div className="w-16 h-16 bg-red-500/20 border border-red-500/30 rounded-xl flex items-center justify-center mb-4 mx-auto">
                <span className="text-red-400 text-2xl">⚠️</span>
              </div>
              <h1 className="text-2xl font-bold text-white mb-2">
                CTAS Application Error
              </h1>
              <p className="text-gray-300">
                Something went wrong while loading the application
              </p>
            </div>
            
            <div className="bg-black/20 rounded-lg p-4 mb-6">
              <h2 className="text-white font-semibold mb-2">Error Details:</h2>
              <div className="text-red-300 text-sm font-mono">
                {this.state.error && this.state.error.toString()}
              </div>
              {this.state.errorInfo && (
                <details className="mt-2">
                  <summary className="text-gray-400 cursor-pointer hover:text-white">
                    Stack Trace (Click to expand)
                  </summary>
                  <pre className="text-xs text-gray-500 mt-2 whitespace-pre-wrap">
                    {this.state.errorInfo.componentStack}
                  </pre>
                </details>
              )}
            </div>

            <div className="flex flex-col sm:flex-row gap-4">
              <button
                onClick={() => window.location.reload()}
                className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
              >
                🔄 Reload Application
              </button>
              <button
                onClick={() => {
                  localStorage.clear();
                  sessionStorage.clear();
                  window.location.reload();
                }}
                className="flex-1 bg-gradient-to-r from-gray-600 to-slate-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-gray-700 hover:to-slate-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
              >
                🧹 Clear Data & Reload
              </button>
            </div>

            <div className="text-center mt-6">
              <p className="text-gray-400 text-sm">
                If this error persists, please check the browser console for more details.
              </p>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
