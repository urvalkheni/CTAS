export default function Alerts() {
  const alerts = [
    {
      id: 1,
      title: "High Tide Warning",
      description: "Unusually high tides expected in coastal areas",
      severity: "high",
      location: "Mumbai Coast",
      timestamp: "2024-01-15T10:30:00Z",
      status: "active"
    },
    {
      id: 2,
      title: "Mangrove Damage Detected",
      description: "Significant damage to mangrove forests reported",
      severity: "medium",
      location: "Goa Coast",
      timestamp: "2024-01-15T09:15:00Z",
      status: "active"
    },
    {
      id: 3,
      title: "Oil Spill Alert",
      description: "Oil spill detected near fishing harbor",
      severity: "critical",
      location: "Chennai Port",
      timestamp: "2024-01-15T08:45:00Z",
      status: "resolved"
    }
  ]

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-100 text-red-800'
      case 'high': return 'bg-orange-100 text-orange-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'low': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusColor = (status: string) => {
    return status === 'active' ? 'bg-red-500' : 'bg-green-500'
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Coastal Alerts</h1>
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors">
            Create Alert
          </button>
        </div>

        <div className="grid gap-6">
          {alerts.map((alert) => (
            <div key={alert.id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {alert.title}
                  </h3>
                  <p className="text-gray-600 mb-3">{alert.description}</p>
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <span>📍 {alert.location}</span>
                    <span>🕒 {new Date(alert.timestamp).toLocaleString()}</span>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${getSeverityColor(alert.severity)}`}>
                    {alert.severity.toUpperCase()}
                  </span>
                  <div className={`w-3 h-3 rounded-full ${getStatusColor(alert.status)}`}></div>
                </div>
              </div>
              
              <div className="flex space-x-3">
                <button className="text-blue-600 hover:text-blue-800 font-medium">
                  View Details
                </button>
                <button className="text-green-600 hover:text-green-800 font-medium">
                  Mark Resolved
                </button>
                <button className="text-gray-600 hover:text-gray-800 font-medium">
                  Share
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
