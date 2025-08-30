'use client';

import { useState } from 'react';

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    profile: {
      name: 'John Doe',
      email: 'john@example.com',
      location: 'Coastal City, CA',
      role: 'Community Member'
    },
    notifications: {
      email: true,
      sms: false,
      highPriority: true,
      weeklyReports: true,
      communityUpdates: false
    },
    privacy: {
      publicProfile: true,
      showOnLeaderboard: true,
      shareLocationData: false,
      allowDataSharing: true
    },
    alerts: {
      stormSurge: true,
      erosion: true,
      waterQuality: true,
      wildlife: false,
      pollution: true,
      weather: true
    }
  });

  const handleProfileChange = (field: string, value: string) => {
    setSettings(prev => ({
      ...prev,
      profile: { ...prev.profile, [field]: value }
    }));
  };

  const handleNotificationChange = (field: string, value: boolean) => {
    setSettings(prev => ({
      ...prev,
      notifications: { ...prev.notifications, [field]: value }
    }));
  };

  const handlePrivacyChange = (field: string, value: boolean) => {
    setSettings(prev => ({
      ...prev,
      privacy: { ...prev.privacy, [field]: value }
    }));
  };

  const handleAlertChange = (field: string, value: boolean) => {
    setSettings(prev => ({
      ...prev,
      alerts: { ...prev.alerts, [field]: value }
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="text-4xl mr-4">⚙️</span>
            Settings
          </h1>
          <p className="text-lg text-gray-600">
            Customize your coastal alert system preferences and account settings
          </p>
        </div>

        <div className="max-w-4xl mx-auto space-y-8">
          {/* Profile Settings */}
          <div className="card">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <span className="text-2xl mr-3">👤</span>
              Profile Settings
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Full Name</label>
                <input 
                  type="text" 
                  value={settings.profile.name}
                  onChange={(e) => handleProfileChange('name', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-ocean-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Email Address</label>
                <input 
                  type="email" 
                  value={settings.profile.email}
                  onChange={(e) => handleProfileChange('email', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-ocean-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Location</label>
                <input 
                  type="text" 
                  value={settings.profile.location}
                  onChange={(e) => handleProfileChange('location', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-ocean-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Role</label>
                <select 
                  value={settings.profile.role}
                  onChange={(e) => handleProfileChange('role', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-ocean-500 focus:border-transparent"
                >
                  <option value="Community Member">Community Member</option>
                  <option value="Researcher">Researcher</option>
                  <option value="Government Official">Government Official</option>
                  <option value="NGO Representative">NGO Representative</option>
                  <option value="Emergency Responder">Emergency Responder</option>
                </select>
              </div>
            </div>
          </div>
          
          {/* Notification Settings */}
          <div className="card">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <span className="text-2xl mr-3">🔔</span>
              Notification Preferences
            </h2>
            <div className="space-y-4">
              {Object.entries(settings.notifications).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                  <div>
                    <span className="text-sm font-semibold text-gray-900 capitalize">
                      {key.replace(/([A-Z])/g, ' $1').trim()}
                    </span>
                    <p className="text-xs text-gray-600 mt-1">
                      {key === 'email' && 'Receive alerts and updates via email'}
                      {key === 'sms' && 'Get critical alerts via SMS messages'}
                      {key === 'highPriority' && 'Immediate notifications for urgent threats'}
                      {key === 'weeklyReports' && 'Weekly summary of coastal conditions'}
                      {key === 'communityUpdates' && 'Updates about community activities'}
                    </p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input 
                      type="checkbox" 
                      checked={value}
                      onChange={(e) => handleNotificationChange(key, e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-ocean-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-ocean-600"></div>
                  </label>
                </div>
              ))}
            </div>
          </div>
          
          {/* Alert Type Settings */}
          <div className="card">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <span className="text-2xl mr-3">🚨</span>
              Alert Type Preferences
            </h2>
            <div className="space-y-4">
              {Object.entries(settings.alerts).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                  <div>
                    <span className="text-sm font-semibold text-gray-900 capitalize">
                      {key.replace(/([A-Z])/g, ' $1').trim()}
                    </span>
                    <p className="text-xs text-gray-600 mt-1">
                      {key === 'stormSurge' && 'Alerts for storm surge and high tide warnings'}
                      {key === 'erosion' && 'Notifications about coastal erosion events'}
                      {key === 'waterQuality' && 'Water quality changes and contamination alerts'}
                      {key === 'wildlife' && 'Wildlife activity and conservation updates'}
                      {key === 'pollution' && 'Pollution incidents and environmental hazards'}
                      {key === 'weather' && 'Severe weather warnings and forecasts'}
                    </p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input 
                      type="checkbox" 
                      checked={value}
                      onChange={(e) => handleAlertChange(key, e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-ocean-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-ocean-600"></div>
                  </label>
                </div>
              ))}
            </div>
          </div>
          
          {/* Privacy Settings */}
          <div className="card">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <span className="text-2xl mr-3">🔒</span>
              Privacy Settings
            </h2>
            <div className="space-y-4">
              {Object.entries(settings.privacy).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                  <div>
                    <span className="text-sm font-semibold text-gray-900 capitalize">
                      {key.replace(/([A-Z])/g, ' $1').trim()}
                    </span>
                    <p className="text-xs text-gray-600 mt-1">
                      {key === 'publicProfile' && 'Allow others to view your profile information'}
                      {key === 'showOnLeaderboard' && 'Display your name on the community leaderboard'}
                      {key === 'shareLocationData' && 'Share location data for improved threat detection'}
                      {key === 'allowDataSharing' && 'Allow anonymized data sharing for research purposes'}
                    </p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input 
                      type="checkbox" 
                      checked={value}
                      onChange={(e) => handlePrivacyChange(key, e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-ocean-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-ocean-600"></div>
                  </label>
                </div>
              ))}
            </div>
          </div>

          {/* Save Button */}
          <div className="flex justify-end space-x-4">
            <button className="btn-secondary">
              Reset to Defaults
            </button>
            <button className="btn-primary">
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}