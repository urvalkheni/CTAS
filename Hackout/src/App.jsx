import { useState, useEffect } from 'react'
import { 
  AlertTriangle, 
  Waves, 
  Wind, 
  Thermometer, 
  MapPin, 
  Bell, 
  Settings, 
  BarChart3,
  Activity,
  Shield,
  Eye,
  Phone,
  Mail,
  Globe,
  Clock
} from 'lucide-react'
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'
import { format, subHours, subDays } from 'date-fns'
import './App.css'

function App() {
  const [currentTime, setCurrentTime] = useState(new Date())
  const [activeAlerts, setActiveAlerts] = useState([])
  const [selectedLocation, setSelectedLocation] = useState('Mumbai Coast')
  const [viewMode, setViewMode] = useState('dashboard')

  // Mock data for demonstration
  const tideData = [
    { time: '00:00', level: 1.2, surge: 0.1 },
    { time: '04:00', level: 2.1, surge: 0.3 },
    { time: '08:00', level: 3.5, surge: 0.8 },
    { time: '12:00', level: 4.2, surge: 1.2 },
    { time: '16:00', level: 3.8, surge: 0.9 },
    { time: '20:00', level: 2.5, surge: 0.4 },
    { time: '24:00', level: 1.8, surge: 0.2 }
  ]

  const weatherData = [
    { time: '00:00', temp: 28, humidity: 75, wind: 12 },
    { time: '04:00', temp: 26, humidity: 80, wind: 15 },
    { time: '08:00', temp: 30, humidity: 70, wind: 18 },
    { time: '12:00', temp: 32, humidity: 65, wind: 22 },
    { time: '16:00', temp: 31, humidity: 68, wind: 20 },
    { time: '20:00', temp: 29, humidity: 72, wind: 16 },
    { time: '24:00', temp: 27, humidity: 78, wind: 14 }
  ]

  const threatData = [
    { name: 'Storm Surge', value: 35, color: '#ef4444' },
    { name: 'Coastal Erosion', value: 25, color: '#f59e0b' },
    { name: 'Pollution', value: 20, color: '#10b981' },
    { name: 'Illegal Activities', value: 15, color: '#8b5cf6' },
    { name: 'Algal Blooms', value: 5, color: '#06b6d4' }
  ]

  const locations = [
    'Mumbai Coast',
    'Chennai Coast', 
    'Kolkata Coast',
    'Kochi Coast',
    'Vishakhapatnam Coast'
  ]

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date())
    }, 1000)

    // Simulate real-time alerts
    const alertTimer = setInterval(() => {
      const newAlert = {
        id: Date.now(),
        type: Math.random() > 0.7 ? 'high' : 'medium',
        message: `Storm surge warning: ${Math.floor(Math.random() * 50) + 20}cm above normal tide levels`,
        location: selectedLocation,
        timestamp: new Date(),
        acknowledged: false
      }
      setActiveAlerts(prev => [newAlert, ...prev.slice(0, 4)])
    }, 30000)

    return () => {
      clearInterval(timer)
      clearInterval(alertTimer)
    }
  }, [selectedLocation])

  const getThreatLevel = (level) => {
    if (level === 'high') return 'bg-red-500'
    if (level === 'medium') return 'bg-yellow-500'
    return 'bg-green-500'
  }

  const acknowledgeAlert = (alertId) => {
    setActiveAlerts(prev => 
      prev.map(alert => 
        alert.id === alertId 
          ? { ...alert, acknowledged: true }
          : alert
      )
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-100">
      {/* Header */}
      <header className="bg-white shadow-lg border-b border-blue-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-600 rounded-lg">
                <Waves className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Coastal Threat Alert System</h1>
                <p className="text-sm text-gray-600">Real-time monitoring & early warning platform</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-gray-600">Current Time</p>
                <p className="text-lg font-mono font-semibold text-gray-900">
                  {format(currentTime, 'HH:mm:ss')}
                </p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600">Date</p>
                <p className="text-lg font-semibold text-gray-900">
                  {format(currentTime, 'MMM dd, yyyy')}
                </p>
              </div>
              <button className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                <Settings className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-blue-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            <button
              onClick={() => setViewMode('dashboard')}
              className={`py-3 px-1 border-b-2 font-medium text-sm ${
                viewMode === 'dashboard'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <BarChart3 className="inline h-4 w-4 mr-2" />
              Dashboard
            </button>
            <button
              onClick={() => setViewMode('alerts')}
              className={`py-3 px-1 border-b-2 font-medium text-sm ${
                viewMode === 'alerts'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Bell className="inline h-4 w-4 mr-2" />
              Alerts
            </button>
            <button
              onClick={() => setViewMode('analytics')}
              className={`py-3 px-1 border-b-2 font-medium text-sm ${
                viewMode === 'analytics'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Activity className="inline h-4 w-4 mr-2" />
              Analytics
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Location Selector */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Monitor Location
          </label>
          <select
            value={selectedLocation}
            onChange={(e) => setSelectedLocation(e.target.value)}
            className="block w-full max-w-xs px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            {locations.map(location => (
              <option key={location} value={location}>{location}</option>
            ))}
          </select>
        </div>

        {viewMode === 'dashboard' && (
          <div className="space-y-6">
            {/* Alert Summary */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                  <AlertTriangle className="h-5 w-5 text-red-500 mr-2" />
                  Active Alerts
                </h2>
                <span className="bg-red-100 text-red-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                  {activeAlerts.filter(a => !a.acknowledged).length} Active
                </span>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {activeAlerts.slice(0, 3).map(alert => (
                  <div key={alert.id} className={`p-4 rounded-lg border-l-4 ${
                    alert.type === 'high' ? 'border-red-500 bg-red-50' : 'border-yellow-500 bg-yellow-50'
                  }`}>
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">{alert.message}</p>
                        <p className="text-xs text-gray-600 mt-1">{alert.location}</p>
                        <p className="text-xs text-gray-500 mt-1">
                          {format(alert.timestamp, 'HH:mm')}
                        </p>
                      </div>
                      {!alert.acknowledged && (
                        <button
                          onClick={() => acknowledgeAlert(alert.id)}
                          className="text-xs bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700"
                        >
                          Ack
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Real-time Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Waves className="h-6 w-6 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Tide Level</p>
                    <p className="text-2xl font-semibold text-gray-900">3.2m</p>
                    <p className="text-xs text-green-600">+0.3m from normal</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <Wind className="h-6 w-6 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Wind Speed</p>
                    <p className="text-2xl font-semibold text-gray-900">18 km/h</p>
                    <p className="text-xs text-yellow-600">Moderate</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-yellow-100 rounded-lg">
                    <Thermometer className="h-6 w-6 text-yellow-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Temperature</p>
                    <p className="text-2xl font-semibold text-gray-900">31°C</p>
                    <p className="text-xs text-gray-600">Humidity: 68%</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <Shield className="h-6 w-6 text-purple-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Threat Level</p>
                    <p className="text-2xl font-semibold text-gray-900">Medium</p>
                    <p className="text-xs text-yellow-600">2 active warnings</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Tide Level Chart */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">24-Hour Tide Levels</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={tideData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="level" stroke="#2563eb" strokeWidth={2} />
                    <Line type="monotone" dataKey="surge" stroke="#dc2626" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
                <div className="mt-4 flex items-center justify-center space-x-6 text-sm">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-blue-600 rounded-full mr-2"></div>
                    <span>Tide Level (m)</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-red-600 rounded-full mr-2"></div>
                    <span>Storm Surge (m)</span>
                  </div>
                </div>
              </div>

              {/* Weather Conditions Chart */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Weather Conditions</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={weatherData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="temp" stackId="1" stroke="#f59e0b" fill="#fef3c7" />
                    <Area type="monotone" dataKey="wind" stackId="2" stroke="#10b981" fill="#d1fae5" />
                  </AreaChart>
                </ResponsiveContainer>
                <div className="mt-4 flex items-center justify-center space-x-6 text-sm">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-yellow-400 rounded-full mr-2"></div>
                    <span>Temperature (°C)</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-green-400 rounded-full mr-2"></div>
                    <span>Wind Speed (km/h)</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Threat Distribution */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Threat Distribution</h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={threatData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {threatData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
                
                <div className="space-y-4">
                  {threatData.map((threat, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center">
                        <div 
                          className="w-4 h-4 rounded-full mr-3"
                          style={{ backgroundColor: threat.color }}
                        ></div>
                        <span className="font-medium text-gray-900">{threat.name}</span>
                      </div>
                      <span className="text-lg font-semibold text-gray-900">{threat.value}%</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {viewMode === 'alerts' && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Alert Management</h2>
            <div className="space-y-4">
              {activeAlerts.map(alert => (
                <div key={alert.id} className={`p-4 rounded-lg border-l-4 ${
                  alert.type === 'high' ? 'border-red-500 bg-red-50' : 'border-yellow-500 bg-yellow-50'
                }`}>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                          alert.type === 'high' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {alert.type.toUpperCase()} PRIORITY
                        </span>
                        <span className="text-xs text-gray-500">
                          {format(alert.timestamp, 'MMM dd, yyyy HH:mm:ss')}
                        </span>
                      </div>
                      <p className="text-sm font-medium text-gray-900 mb-1">{alert.message}</p>
                      <p className="text-xs text-gray-600">Location: {alert.location}</p>
                    </div>
                    <div className="flex space-x-2">
                      {!alert.acknowledged && (
                        <button
                          onClick={() => acknowledgeAlert(alert.id)}
                          className="px-3 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700"
                        >
                          Acknowledge
                        </button>
                      )}
                      <button className="px-3 py-1 bg-gray-600 text-white text-xs rounded hover:bg-gray-700">
                        Details
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {viewMode === 'analytics' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Historical Trends</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <p className="text-2xl font-bold text-blue-600">24</p>
                  <p className="text-sm text-gray-600">Alerts this week</p>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <p className="text-2xl font-bold text-green-600">89%</p>
                  <p className="text-sm text-gray-600">Response rate</p>
                </div>
                <div className="text-center p-4 bg-yellow-50 rounded-lg">
                  <p className="text-2xl font-bold text-yellow-600">12min</p>
                  <p className="text-sm text-gray-600">Avg response time</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-4">Coastal Threat Alert System</h3>
              <p className="text-gray-300 text-sm">
                Protecting coastal communities through real-time monitoring and early warning systems.
              </p>
            </div>
            <div>
              <h4 className="font-medium mb-4">Quick Actions</h4>
              <ul className="space-y-2 text-sm text-gray-300">
                <li><button className="hover:text-white">Report Incident</button></li>
                <li><button className="hover:text-white">Subscribe to Alerts</button></li>
                <li><button className="hover:text-white">Emergency Contacts</button></li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium mb-4">Contact</h4>
              <ul className="space-y-2 text-sm text-gray-300">
                <li className="flex items-center">
                  <Phone className="h-4 w-4 mr-2" />
                  Emergency: 100
                </li>
                <li className="flex items-center">
                  <Mail className="h-4 w-4 mr-2" />
                  alerts@coastal.gov.in
                </li>
                <li className="flex items-center">
                  <Globe className="h-4 w-4 mr-2" />
                  www.coastal.gov.in
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium mb-4">System Status</h4>
              <div className="space-y-2 text-sm">
                <div className="flex items-center">
                  <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                  <span className="text-gray-300">All systems operational</span>
                </div>
                <div className="flex items-center">
                  <Clock className="h-4 w-4 mr-2 text-gray-300" />
                  <span className="text-gray-300">Uptime: 99.9%</span>
                </div>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-sm text-gray-300">
            <p>&copy; 2024 Coastal Threat Alert System. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
