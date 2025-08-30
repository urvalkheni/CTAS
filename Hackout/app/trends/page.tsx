export default function TrendsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Coastal Trends</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Water Quality Trends</h2>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span>Bacteria Levels</span>
              <span className="text-green-600">↓ 15%</span>
            </div>
            <div className="flex justify-between items-center">
              <span>Water Clarity</span>
              <span className="text-green-600">↑ 8%</span>
            </div>
            <div className="flex justify-between items-center">
              <span>pH Levels</span>
              <span className="text-yellow-600">→ Stable</span>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Weather Patterns</h2>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span>Average Temperature</span>
              <span className="text-red-600">↑ 2.3°C</span>
            </div>
            <div className="flex justify-between items-center">
              <span>Rainfall</span>
              <span className="text-blue-600">↓ 12%</span>
            </div>
            <div className="flex justify-between items-center">
              <span>Wind Speed</span>
              <span className="text-yellow-600">↑ 5%</span>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Beach Conditions</h2>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span>Erosion Rate</span>
              <span className="text-red-600">↑ 8%</span>
            </div>
            <div className="flex justify-between items-center">
              <span>Sand Quality</span>
              <span className="text-green-600">↑ 3%</span>
            </div>
            <div className="flex justify-between items-center">
              <span>Accessibility</span>
              <span className="text-green-600">↑ 12%</span>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Wildlife Activity</h2>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span>Sea Turtle Sightings</span>
              <span className="text-green-600">↑ 25%</span>
            </div>
            <div className="flex justify-between items-center">
              <span>Bird Populations</span>
              <span className="text-green-600">↑ 18%</span>
            </div>
            <div className="flex justify-between items-center">
              <span>Fish Diversity</span>
              <span className="text-yellow-600">→ Stable</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
