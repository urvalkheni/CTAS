export default function AlertsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Coastal Alerts</h1>
      <div className="space-y-4">
        <div className="bg-red-50 border border-red-200 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-red-800">High Tide Warning</h3>
          <p className="text-red-700">Expected high tide at 2:30 PM today. Coastal flooding possible.</p>
          <span className="text-sm text-red-600">Posted 2 hours ago</span>
        </div>
        <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-yellow-800">Storm Watch</h3>
          <p className="text-yellow-700">Strong winds expected tomorrow. Secure loose objects.</p>
          <span className="text-sm text-yellow-600">Posted 4 hours ago</span>
        </div>
        <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-blue-800">Water Quality Alert</h3>
          <p className="text-blue-700">Elevated bacteria levels detected at Main Beach.</p>
          <span className="text-sm text-blue-600">Posted 6 hours ago</span>
        </div>
      </div>
    </div>
  );
}
