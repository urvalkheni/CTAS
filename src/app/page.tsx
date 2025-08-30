'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface DashboardStats {
  activeAlerts: number;
  reportsToday: number;
  userRank: number;
  threatLevel: 'low' | 'medium' | 'high' | 'critical';
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats>({
    activeAlerts: 3,
    reportsToday: 12,
    userRank: 5,
    threatLevel: 'medium'
  });

  const [recentAlerts, setRecentAlerts] = useState([
    {
      id: '1',
      type: 'Storm Surge',
      severity: 'critical',
      location: 'North Bay',
      time: '15 min ago'
    },
    {
      id: '2',
      type: 'High Tide',
      severity: 'warning',
      location: 'Main Beach',
      time: '2 hours ago'
    },
    {
      id: '3',
      type: 'Water Quality',
      severity: 'alert',
      location: 'South Harbor',
      time: '4 hours ago'
    }
  ]);

  const getThreatLevelColor = (level: string) => {
    switch (level) {
      case 'critical': return 'text-coral-600 bg-coral-50';
      case 'high': return 'text-coral-500 bg-coral-50';
      case 'medium': return 'text-sand-600 bg-sand-50';
      case 'low': return 'text-emerald-600 bg-emerald-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-coral-500';
      case 'warning': return 'bg-sand-500';
      case 'alert': return 'bg-ocean-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Hero Section */}
      <div className="gradient-hero text-white py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl font-bold mb-6 leading-tight">
              Coastal Threat Alert System
            </h1>
            <p className="text-xl text-blue-100 mb-8 leading-relaxed">
              Comprehensive early warning platform protecting coastal communities through 
              AI-powered threat detection, real-time monitoring, and instant alerts
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/alerts" className="btn-primary bg-white text-ocean-700 hover:bg-gray-100">
                View Active Alerts
              </Link>
              <Link href="/reports" className="btn-secondary bg-transparent border-white text-white hover:bg-white/10">
                Submit Report
              </Link>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12">
        {/* Current Threat Level */}
        <div className="mb-12">
          <div className="card max-w-md mx-auto text-center">
            <h2 className="text-2xl font-bold mb-4">Current Threat Level</h2>
            <div className={`inline-flex items-center px-6 py-3 rounded-full text-lg font-semibold ${getThreatLevelColor(stats.threatLevel)}`}>
              <div className={`w-3 h-3 rounded-full mr-3 ${stats.threatLevel === 'critical' ? 'bg-coral-500' : stats.threatLevel === 'high' ? 'bg-coral-400' : stats.threatLevel === 'medium' ? 'bg-sand-500' : 'bg-emerald-500'}`}></div>
              {stats.threatLevel.toUpperCase()}
            </div>
            <p className="text-gray-600 mt-4 text-sm">
              Based on current sensor data and AI analysis
            </p>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div className="card text-center group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-coral-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🚨</span>
            </div>
            <h3 className="text-3xl font-bold text-coral-600 mb-2">{stats.activeAlerts}</h3>
            <p className="text-gray-600 font-medium">Active Alerts</p>
            <p className="text-sm text-gray-500 mt-2">Requiring immediate attention</p>
          </div>

          <div className="card text-center group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-ocean-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">📊</span>
            </div>
            <h3 className="text-3xl font-bold text-ocean-600 mb-2">{stats.reportsToday}</h3>
            <p className="text-gray-600 font-medium">Reports Today</p>
            <p className="text-sm text-gray-500 mt-2">Community submissions</p>
          </div>

          <div className="card text-center group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🏆</span>
            </div>
            <h3 className="text-3xl font-bold text-emerald-600 mb-2">#{stats.userRank}</h3>
            <p className="text-gray-600 font-medium">Your Rank</p>
            <p className="text-sm text-gray-500 mt-2">Community leaderboard</p>
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="card">
            <h2 className="text-2xl font-bold mb-6 flex items-center">
              <span className="text-2xl mr-3">⚡</span>
              Recent Alerts
            </h2>
            <div className="space-y-4">
              {recentAlerts.map((alert) => (
                <div key={alert.id} className="flex items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                  <div className={`w-4 h-4 rounded-full mr-4 ${getSeverityColor(alert.severity)}`}></div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-900">{alert.type}</h4>
                    <p className="text-sm text-gray-600">{alert.location}</p>
                  </div>
                  <span className="text-xs text-gray-500">{alert.time}</span>
                </div>
              ))}
            </div>
            <Link href="/alerts" className="block mt-6 text-ocean-600 hover:text-ocean-700 font-medium text-center">
              View All Alerts →
            </Link>
          </div>

          {/* Quick Actions */}
          <div className="card">
            <h2 className="text-2xl font-bold mb-6 flex items-center">
              <span className="text-2xl mr-3">🎯</span>
              Quick Actions
            </h2>
            <div className="space-y-4">
              <Link href="/reports" className="block p-4 bg-ocean-50 rounded-lg hover:bg-ocean-100 transition-colors duration-200 group">
                <div className="flex items-center">
                  <span className="text-2xl mr-4">📝</span>
                  <div>
                    <h4 className="font-semibold text-gray-900 group-hover:text-ocean-700">Submit Report</h4>
                    <p className="text-sm text-gray-600">Report coastal threats or observations</p>
                  </div>
                </div>
              </Link>
              
              <Link href="/trends" className="block p-4 bg-emerald-50 rounded-lg hover:bg-emerald-100 transition-colors duration-200 group">
                <div className="flex items-center">
                  <span className="text-2xl mr-4">📈</span>
                  <div>
                    <h4 className="font-semibold text-gray-900 group-hover:text-emerald-700">View Trends</h4>
                    <p className="text-sm text-gray-600">Analyze coastal condition patterns</p>
                  </div>
                </div>
              </Link>
              
              <Link href="/leaderboard" className="block p-4 bg-sand-50 rounded-lg hover:bg-sand-100 transition-colors duration-200 group">
                <div className="flex items-center">
                  <span className="text-2xl mr-4">🏆</span>
                  <div>
                    <h4 className="font-semibold text-gray-900 group-hover:text-sand-700">Community Leaderboard</h4>
                    <p className="text-sm text-gray-600">See top contributors</p>
                  </div>
                </div>
              </Link>
            </div>
          </div>
        </div>

        {/* System Status */}
        <div className="mt-12">
          <div className="card">
            <h2 className="text-2xl font-bold mb-6 flex items-center">
              <span className="text-2xl mr-3">🔧</span>
              System Status
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="w-3 h-3 bg-emerald-500 rounded-full mx-auto mb-2"></div>
                <p className="text-sm font-medium text-gray-900">Sensors</p>
                <p className="text-xs text-gray-500">98% Online</p>
              </div>
              <div className="text-center">
                <div className="w-3 h-3 bg-emerald-500 rounded-full mx-auto mb-2"></div>
                <p className="text-sm font-medium text-gray-900">Satellite Feed</p>
                <p className="text-xs text-gray-500">Active</p>
              </div>
              <div className="text-center">
                <div className="w-3 h-3 bg-sand-500 rounded-full mx-auto mb-2"></div>
                <p className="text-sm font-medium text-gray-900">AI Analysis</p>
                <p className="text-xs text-gray-500">Processing</p>
              </div>
              <div className="text-center">
                <div className="w-3 h-3 bg-emerald-500 rounded-full mx-auto mb-2"></div>
                <p className="text-sm font-medium text-gray-900">Alert System</p>
                <p className="text-xs text-gray-500">Operational</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}