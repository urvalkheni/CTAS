export default function LeaderboardPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Community Leaderboard</h1>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rank</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reports</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Points</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            <tr>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">1</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">Sarah Wilson</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">45</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">1,250</td>
            </tr>
            <tr>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">2</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">Mike Johnson</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">38</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">1,120</td>
            </tr>
            <tr>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">3</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">Emily Davis</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">32</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">980</td>
            </tr>
            <tr>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">4</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">David Brown</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">28</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">850</td>
            </tr>
            <tr>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">5</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">Lisa Chen</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">25</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">720</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
