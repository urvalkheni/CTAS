export default function Reports() {
  const reports = [
    {
      id: 1,
      title: "Mangrove Restoration Progress",
      type: "conservation",
      author: "Dr. Sarah Johnson",
      location: "Mumbai Coast",
      date: "2024-01-15",
      status: "published"
    },
    {
      id: 2,
      title: "Water Quality Analysis",
      type: "monitoring",
      author: "Environmental Team",
      location: "Goa Beach",
      date: "2024-01-14",
      status: "draft"
    },
    {
      id: 3,
      title: "Coastal Erosion Study",
      type: "research",
      author: "Prof. Michael Chen",
      location: "Chennai Coast",
      date: "2024-01-13",
      status: "published"
    }
  ]

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'conservation': return 'bg-green-100 text-green-800'
      case 'monitoring': return 'bg-blue-100 text-blue-800'
      case 'research': return 'bg-purple-100 text-purple-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Reports</h1>
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors">
            Create Report
          </button>
        </div>

        <div className="grid gap-6">
          {reports.map((report) => (
            <div key={report.id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {report.title}
                  </h3>
                  <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
                    <span>👤 {report.author}</span>
                    <span>📍 {report.location}</span>
                    <span>📅 {report.date}</span>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${getTypeColor(report.type)}`}>
                    {report.type.toUpperCase()}
                  </span>
                  {report.status === 'draft' && (
                    <span className="px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                      DRAFT
                    </span>
                  )}
                </div>
              </div>
              
              <div className="flex space-x-3">
                <button className="text-blue-600 hover:text-blue-800 font-medium">
                  View Report
                </button>
                <button className="text-green-600 hover:text-green-800 font-medium">
                  Download PDF
                </button>
                <button className="text-gray-600 hover:text-gray-800 font-medium">
                  Share
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-8 bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Report Categories</h2>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="p-4 bg-green-50 rounded-lg">
              <h3 className="font-semibold text-green-800 mb-2">Conservation</h3>
              <p className="text-sm text-green-600">Mangrove restoration and protection projects</p>
            </div>
            <div className="p-4 bg-blue-50 rounded-lg">
              <h3 className="font-semibold text-blue-800 mb-2">Monitoring</h3>
              <p className="text-sm text-blue-600">Environmental monitoring and data collection</p>
            </div>
            <div className="p-4 bg-purple-50 rounded-lg">
              <h3 className="font-semibold text-purple-800 mb-2">Research</h3>
              <p className="text-sm text-purple-600">Scientific studies and analysis</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
