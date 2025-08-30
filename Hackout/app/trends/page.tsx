export default function Trends() {
  const trendData = {
    alerts: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      data: [12, 19, 15, 25, 22, 30]
    },
    reports: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      data: [45, 52, 48, 65, 58, 72]
    },
    conservation: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      data: [8, 12, 10, 15, 18, 22]
    }
  }

  const topTrends = [
    {
      title: "Mangrove Restoration",
      change: "+15%",
      trend: "up",
      description: "Increased focus on mangrove conservation projects"
    },
    {
      title: "Water Quality Monitoring",
      change: "+8%",
      trend: "up",
      description: "More frequent water quality assessments"
    },
    {
      title: "Coastal Erosion",
      change: "-12%",
      trend: "down",
      description: "Reduced erosion incidents due to protection measures"
    },
    {
      title: "Community Engagement",
      change: "+23%",
      trend: "up",
      description: "Growing community participation in coastal protection"
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Trends & Analytics</h1>
        
        <div className="grid lg:grid-cols-3 gap-8 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Alerts Trend</h3>
            <div className="space-y-2">
              {trendData.alerts.data.map((value, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <div className="w-8 text-sm text-gray-500">{trendData.alerts.labels[index]}</div>
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-red-500 h-2 rounded-full" 
                      style={{ width: `${(value / 30) * 100}%` }}
                    ></div>
                  </div>
                  <div className="w-8 text-sm font-medium">{value}</div>
                </div>
              ))}
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Reports Trend</h3>
            <div className="space-y-2">
              {trendData.reports.data.map((value, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <div className="w-8 text-sm text-gray-500">{trendData.reports.labels[index]}</div>
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-500 h-2 rounded-full" 
                      style={{ width: `${(value / 72) * 100}%` }}
                    ></div>
                  </div>
                  <div className="w-8 text-sm font-medium">{value}</div>
                </div>
              ))}
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Conservation Projects</h3>
            <div className="space-y-2">
              {trendData.conservation.data.map((value, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <div className="w-8 text-sm text-gray-500">{trendData.conservation.labels[index]}</div>
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-green-500 h-2 rounded-full" 
                      style={{ width: `${(value / 22) * 100}%` }}
                    ></div>
                  </div>
                  <div className="w-8 text-sm font-medium">{value}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Top Trends</h3>
            <div className="space-y-4">
              {topTrends.map((trend, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <h4 className="font-medium text-gray-900">{trend.title}</h4>
                    <p className="text-sm text-gray-600">{trend.description}</p>
                  </div>
                  <div className={`flex items-center space-x-1 ${
                    trend.trend === 'up' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    <span className="text-lg">
                      {trend.trend === 'up' ? '↗' : '↘'}
                    </span>
                    <span className="font-semibold">{trend.change}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Key Insights</h3>
            <div className="space-y-4">
              <div className="p-4 bg-blue-50 rounded-lg">
                <h4 className="font-medium text-blue-900 mb-2">Community Growth</h4>
                <p className="text-sm text-blue-700">
                  Community participation has increased by 23% this quarter, 
                  showing strong engagement in coastal protection initiatives.
                </p>
              </div>
              
              <div className="p-4 bg-green-50 rounded-lg">
                <h4 className="font-medium text-green-900 mb-2">Conservation Success</h4>
                <p className="text-sm text-green-700">
                  Mangrove restoration projects have shown 15% improvement 
                  in survival rates due to better monitoring and care.
                </p>
              </div>
              
              <div className="p-4 bg-yellow-50 rounded-lg">
                <h4 className="font-medium text-yellow-900 mb-2">Alert Efficiency</h4>
                <p className="text-sm text-yellow-700">
                  Response time to coastal alerts has improved by 40% 
                  through better coordination and communication systems.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-8 bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4">Regional Analysis</h3>
          <div className="grid md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <h4 className="font-medium text-gray-900">Mumbai Coast</h4>
              <p className="text-2xl font-bold text-blue-600">156</p>
              <p className="text-sm text-gray-500">reports this month</p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <h4 className="font-medium text-gray-900">Goa Coast</h4>
              <p className="text-2xl font-bold text-green-600">89</p>
              <p className="text-sm text-gray-500">reports this month</p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <h4 className="font-medium text-gray-900">Chennai Coast</h4>
              <p className="text-2xl font-bold text-purple-600">124</p>
              <p className="text-sm text-gray-500">reports this month</p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <h4 className="font-medium text-gray-900">Kerala Coast</h4>
              <p className="text-2xl font-bold text-orange-600">67</p>
              <p className="text-sm text-gray-500">reports this month</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
