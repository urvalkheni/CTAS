'use client';

import { useState } from 'react';

export default function TrendsPage() {
  const [selectedTimeframe, setSelectedTimeframe] = useState('30d');

  const trendData = {
    waterQuality: {
      bacteriaLevels: { value: -15, trend: 'down', status: 'improving' },
      waterClarity: { value: 8, trend: 'up', status: 'improving' },
      phLevels: { value: 0, trend: 'stable', status: 'stable' },
      temperature: { value: 2.3, trend: 'up', status: 'concerning' }
    },
    weatherPatterns: {
      avgTemperature: { value: 2.3, trend: 'up', status: 'concerning' },
      rainfall: { value: -12, trend: 'down', status: 'concerning' },
      windSpeed: { value: 5, trend: 'up', status: 'normal' },
      stormFrequency: { value: 15, trend: 'up', status: 'concerning' }
    },
    beachConditions: {
      erosionRate: { value: 8, trend: 'up', status: 'concerning' },
      sandQuality: { value: 3, trend: 'up', status: 'improving' },
      accessibility: { value: 12, trend: 'up', status: 'improving' },
      vegetation: { value: -5, trend: 'down', status: 'concerning' }
    },
    wildlifeActivity: {
      seaTurtles: { value: 25, trend: 'up', status: 'improving' },
      birdPopulations: { value: 18, trend: 'up', status: 'improving' },
      fishDiversity: { value: 0, trend: 'stable', status: 'stable' },
      coralHealth: { value: -8, trend: 'down', status: 'concerning' }
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return '↗️';
      case 'down': return '↘️';
      case 'stable': return '➡️';
      default: return '➡️';
    }
  };

  const getTrendColor = (status: string) => {
    switch (status) {
      case 'improving': return 'text-emerald-600';
      case 'concerning': return 'text-coral-600';
      case 'stable': return 'text-sand-600';
      default: return 'text-gray-600';
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'improving': return 'bg-emerald-100 text-emerald-800';
      case 'concerning': return 'bg-coral-100 text-coral-800';
      case 'stable': return 'bg-sand-100 text-sand-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="text-4xl mr-4">📈</span>
            Coastal Trends Analysis
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl">
            AI-powered analysis of coastal conditions using sensor data, satellite imagery, 
            and historical patterns to identify emerging threats and long-term changes.
          </p>
        </div>

        {/* Timeframe Selector */}
        <div className="mb-8">
          <div className="flex space-x-2">
            {['7d', '30d', '90d', '1y'].map((timeframe) => (
              <button
                key={timeframe}
                onClick={() => setSelectedTimeframe(timeframe)}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                  selectedTimeframe === timeframe
                    ? 'bg-ocean-600 text-white shadow-md'
                    : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
                }`}
              >
                {timeframe === '7d' ? 'Last 7 Days' : 
                 timeframe === '30d' ? 'Last 30 Days' :
                 timeframe === '90d' ? 'Last 3 Months' : 'Last Year'}
              </button>
            ))}
          </div>
        </div>

        {/* Trends Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Water Quality Trends */}
          <div className="card">
            <h2 className="text-2xl font-bold mb-6 flex items-center text-ocean-700">
              <span className="text-2xl mr-3">💧</span>
              Water Quality Trends
            </h2>
            <div className="space-y-4">
              {Object.entries(trendData.waterQuality).map(([key, data]) => (
                <div key={key} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                  <div className="flex items-center space-x-3">
                    <span className="text-lg">{getTrendIcon(data.trend)}</span>
                    <div>
                      <p className="font-semibold text-gray-900 capitalize">
                        {key.replace(/([A-Z])/g, ' $1').trim()}
                      </p>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusBadge(data.status)}`}>
                        {data.status}
                      </span>
                    </div>
                  </div>
                  <span className={`text-lg font-bold ${getTrendColor(data.status)}`}>
                    {data.value > 0 ? '+' : ''}{data.value}%
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Weather Patterns */}
          <div className="card">
            <h2 className="text-2xl font-bold mb-6 flex items-center text-sand-700">
              <span className="text-2xl mr-3">🌤️</span>
              Weather Patterns
            </h2>
            <div className="space-y-4">
              {Object.entries(trendData.weatherPatterns).map(([key, data]) => (
                <div key={key} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                  <div className="flex items-center space-x-3">
                    <span className="text-lg">{getTrendIcon(data.trend)}</span>
                    <div>
                      <p className="font-semibold text-gray-900 capitalize">
                        {key.replace(/([A-Z])/g, ' $1').trim()}
                      </p>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusBadge(data.status)}`}>
                        {data.status}
                      </span>
                    </div>
                  </div>
                  <span className={`text-lg font-bold ${getTrendColor(data.status)}`}>
                    {data.value > 0 ? '+' : ''}{data.value}%
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Beach Conditions */}
          <div className="card">
            <h2 className="text-2xl font-bold mb-6 flex items-center text-sand-700">
              <span className="text-2xl mr-3">🏖️</span>
              Beach Conditions
            </h2>
            <div className="space-y-4">
              {Object.entries(trendData.beachConditions).map(([key, data]) => (
                <div key={key} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                  <div className="flex items-center space-x-3">
                    <span className="text-lg">{getTrendIcon(data.trend)}</span>
                    <div>
                      <p className="font-semibold text-gray-900 capitalize">
                        {key.replace(/([A-Z])/g, ' $1').trim()}
                      </p>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusBadge(data.status)}`}>
                        {data.status}
                      </span>
                    </div>
                  </div>
                  <span className={`text-lg font-bold ${getTrendColor(data.status)}`}>
                    {data.value > 0 ? '+' : ''}{data.value}%
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Wildlife Activity */}
          <div className="card">
            <h2 className="text-2xl font-bold mb-6 flex items-center text-emerald-700">
              <span className="text-2xl mr-3">🐢</span>
              Wildlife Activity
            </h2>
            <div className="space-y-4">
              {Object.entries(trendData.wildlifeActivity).map(([key, data]) => (
                <div key={key} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                  <div className="flex items-center space-x-3">
                    <span className="text-lg">{getTrendIcon(data.trend)}</span>
                    <div>
                      <p className="font-semibold text-gray-900 capitalize">
                        {key.replace(/([A-Z])/g, ' $1').trim()}
                      </p>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusBadge(data.status)}`}>
                        {data.status}
                      </span>
                    </div>
                  </div>
                  <span className={`text-lg font-bold ${getTrendColor(data.status)}`}>
                    {data.value > 0 ? '+' : ''}{data.value}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* AI Insights */}
        <div className="mt-12">
          <div className="card bg-gradient-to-r from-ocean-50 to-blue-50 border-ocean-200">
            <h2 className="text-2xl font-bold text-ocean-800 mb-6 flex items-center">
              <span className="text-2xl mr-3">🤖</span>
              AI-Powered Insights
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-4 rounded-lg">
                <h4 className="font-semibold text-gray-900 mb-2">Threat Prediction</h4>
                <p className="text-sm text-gray-700">
                  Based on current patterns, elevated storm surge risk predicted for next 72 hours. 
                  Recommend increased monitoring of vulnerable areas.
                </p>
              </div>
              <div className="bg-white p-4 rounded-lg">
                <h4 className="font-semibold text-gray-900 mb-2">Anomaly Detection</h4>
                <p className="text-sm text-gray-700">
                  Unusual temperature patterns detected in North Bay. Potential algal bloom 
                  conditions developing. Enhanced water quality monitoring recommended.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}