'use client';

import { useState, useEffect } from 'react';

interface Alert {
  id: string;
  type: string;
  severity: 'info' | 'warning' | 'alert' | 'critical';
  title: string;
  message: string;
  location: string;
  timestamp: string;
  active: boolean;
}

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [filter, setFilter] = useState<string>('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await fetch('/api/alerts');
      const data = await response.json();
      if (data.success) {
        setAlerts(data.alerts);
      }
    } catch (error) {
      console.error('Failed to fetch alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical': return '🔴';
      case 'alert': return '🟠';
      case 'warning': return '🟡';
      case 'info': return '🔵';
      default: return '⚪';
    }
  };

  const getSeverityClass = (severity: string) => {
    switch (severity) {
      case 'critical': return 'alert-critical border-l-4 border-l-coral-500';
      case 'alert': return 'bg-coral-50 border-coral-200 text-coral-800 border-l-4 border-l-coral-400';
      case 'warning': return 'alert-warning border-l-4 border-l-sand-500';
      case 'info': return 'alert-info border-l-4 border-l-ocean-500';
      default: return 'bg-gray-50 border-gray-200 text-gray-800';
    }
  };

  const filteredAlerts = filter === 'all' ? alerts : alerts.filter(alert => alert.severity === filter);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-ocean-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading alerts...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="text-4xl mr-4">🚨</span>
            Coastal Threat Alerts
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl">
            Real-time alerts from our AI-powered monitoring system analyzing sensor data, 
            satellite feeds, and historical patterns to detect coastal threats.
          </p>
        </div>

        {/* Filter Tabs */}
        <div className="mb-8">
          <div className="flex flex-wrap gap-2">
            {['all', 'critical', 'alert', 'warning', 'info'].map((severity) => (
              <button
                key={severity}
                onClick={() => setFilter(severity)}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                  filter === severity
                    ? 'bg-ocean-600 text-white shadow-md'
                    : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
                }`}
              >
                {severity === 'all' ? 'All Alerts' : severity.charAt(0).toUpperCase() + severity.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Alerts List */}
        <div className="space-y-6">
          {filteredAlerts.length === 0 ? (
            <div className="card text-center py-12">
              <span className="text-6xl mb-4 block">🌊</span>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No alerts found</h3>
              <p className="text-gray-600">
                {filter === 'all' ? 'All systems are currently normal.' : `No ${filter} alerts at this time.`}
              </p>
            </div>
          ) : (
            filteredAlerts.map((alert) => (
              <div key={alert.id} className={`card ${getSeverityClass(alert.severity)} hover:shadow-lg transition-all duration-200`}>
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-4 flex-1">
                    <div className="text-3xl">{getSeverityIcon(alert.severity)}</div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-xl font-bold">{alert.title}</h3>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wide ${getSeverityClass(alert.severity)}`}>
                          {alert.severity}
                        </span>
                      </div>
                      <p className="text-gray-700 mb-3 leading-relaxed">{alert.message}</p>
                      <div className="flex items-center space-x-6 text-sm text-gray-600">
                        <div className="flex items-center">
                          <span className="mr-2">📍</span>
                          <span className="font-medium">{alert.location}</span>
                        </div>
                        <div className="flex items-center">
                          <span className="mr-2">🕒</span>
                          <span>{new Date(alert.timestamp).toLocaleString()}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="flex space-x-2 ml-4">
                    <button className="btn-secondary text-sm py-2 px-4">
                      Details
                    </button>
                    <button className="btn-primary text-sm py-2 px-4">
                      Acknowledge
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Emergency Contact */}
        <div className="mt-12">
          <div className="card bg-coral-50 border-coral-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <span className="text-3xl mr-4">📞</span>
                <div>
                  <h3 className="text-xl font-bold text-coral-800">Emergency Contact</h3>
                  <p className="text-coral-700">For immediate assistance during critical threats</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-coral-800">911</p>
                <p className="text-sm text-coral-600">Emergency Services</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}