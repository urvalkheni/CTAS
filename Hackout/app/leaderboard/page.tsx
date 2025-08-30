export default function Leaderboard() {
  const leaderboardData = [
    {
      rank: 1,
      name: "Dr. Sarah Johnson",
      organization: "Marine Conservation Society",
      points: 2847,
      reports: 45,
      alerts: 12,
      avatar: "👩‍🔬"
    },
    {
      rank: 2,
      name: "Prof. Michael Chen",
      organization: "Ocean Research Institute",
      points: 2653,
      reports: 38,
      alerts: 8,
      avatar: "👨‍🏫"
    },
    {
      rank: 3,
      name: "Environmental Team Alpha",
      organization: "Coastal Protection NGO",
      points: 2412,
      reports: 52,
      alerts: 15,
      avatar: "👥"
    },
    {
      rank: 4,
      name: "Dr. Emily Rodriguez",
      organization: "Mangrove Restoration Project",
      points: 2189,
      reports: 31,
      alerts: 6,
      avatar: "👩‍🌾"
    },
    {
      rank: 5,
      name: "Coastal Watch Group",
      organization: "Community Volunteers",
      points: 1956,
      reports: 28,
      alerts: 9,
      avatar: "👥"
    }
  ]

  const getRankBadge = (rank: number) => {
    switch (rank) {
      case 1: return "🥇"
      case 2: return "🥈"
      case 3: return "🥉"
      default: return `#${rank}`
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Community Leaderboard</h1>
        
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-cyan-600 px-6 py-4">
            <h2 className="text-xl font-semibold text-white">Top Contributors</h2>
            <p className="text-blue-100">Recognizing our most active community members</p>
          </div>
          
          <div className="p-6">
            <div className="space-y-4">
              {leaderboardData.map((member) => (
                <div key={member.rank} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                  <div className="flex-shrink-0">
                    <span className="text-2xl">{getRankBadge(member.rank)}</span>
                  </div>
                  
                  <div className="flex-shrink-0">
                    <span className="text-3xl">{member.avatar}</span>
                  </div>
                  
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900">{member.name}</h3>
                    <p className="text-sm text-gray-600">{member.organization}</p>
                  </div>
                  
                  <div className="text-right">
                    <div className="text-2xl font-bold text-blue-600">{member.points}</div>
                    <div className="text-sm text-gray-500">points</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-sm font-medium text-gray-900">{member.reports}</div>
                    <div className="text-xs text-gray-500">reports</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-sm font-medium text-gray-900">{member.alerts}</div>
                    <div className="text-xs text-gray-500">alerts</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-8 grid md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">How Points Work</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span>Submit Report</span>
                <span className="font-medium">+50 points</span>
              </div>
              <div className="flex justify-between">
                <span>Create Alert</span>
                <span className="font-medium">+25 points</span>
              </div>
              <div className="flex justify-between">
                <span>Resolve Alert</span>
                <span className="font-medium">+100 points</span>
              </div>
              <div className="flex justify-between">
                <span>Community Engagement</span>
                <span className="font-medium">+10 points</span>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">This Month's Stats</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span>Total Reports</span>
                <span className="font-medium">1,247</span>
              </div>
              <div className="flex justify-between">
                <span>Active Alerts</span>
                <span className="font-medium">89</span>
              </div>
              <div className="flex justify-between">
                <span>Community Members</span>
                <span className="font-medium">5,432</span>
              </div>
              <div className="flex justify-between">
                <span>Projects Completed</span>
                <span className="font-medium">23</span>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Achievements</h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <span className="text-yellow-500">🏆</span>
                <span className="text-sm">First Report</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-yellow-500">🎯</span>
                <span className="text-sm">Alert Master</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-yellow-500">🌱</span>
                <span className="text-sm">Conservation Hero</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-yellow-500">📊</span>
                <span className="text-sm">Data Analyst</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
