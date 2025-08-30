export default function ReportsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Coastal Reports</h1>
      <div className="mb-6">
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          Create New Report
        </button>
      </div>
      <div className="space-y-4">
        <div className="bg-white p-4 rounded-lg shadow border">
          <h3 className="text-lg font-semibold">Beach Erosion Report</h3>
          <p className="text-gray-600">Significant erosion observed at North Beach</p>
          <div className="flex justify-between items-center mt-2">
            <span className="text-sm text-gray-500">Submitted by: John Doe</span>
            <span className="text-sm text-gray-500">2 hours ago</span>
          </div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow border">
          <h3 className="text-lg font-semibold">Water Quality Report</h3>
          <p className="text-gray-600">Water clarity improved at South Bay</p>
          <div className="flex justify-between items-center mt-2">
            <span className="text-sm text-gray-500">Submitted by: Jane Smith</span>
            <span className="text-sm text-gray-500">5 hours ago</span>
          </div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow border">
          <h3 className="text-lg font-semibold">Wildlife Sighting</h3>
          <p className="text-gray-600">Sea turtle nesting activity observed</p>
          <div className="flex justify-between items-center mt-2">
            <span className="text-sm text-gray-500">Submitted by: Mike Johnson</span>
            <span className="text-sm text-gray-500">1 day ago</span>
          </div>
        </div>
      </div>
    </div>
  );
}
