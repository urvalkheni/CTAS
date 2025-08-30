import Link from 'next/link'
import ThemeToggle from '@/components/ThemeToggle'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-cyan-50 to-teal-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Navigation */}
      <nav className="glass border-b border-gray-200 dark:border-gray-700">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <span className="text-2xl">🌊</span>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">Coastal Protection Platform</h1>
            </div>
            <div className="flex items-center space-x-4">
              <ThemeToggle />
              <Link 
                href="/login" 
                className="px-4 py-2 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-medium transition-colors"
              >
                Login
              </Link>
              <Link 
                href="/register" 
                className="btn-primary"
              >
                Register
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
            Protect Our
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-cyan">
              {" "}Coastlines
            </span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
            Real-time coastal threat monitoring and community-driven mangrove conservation platform. 
            Join authorities, NGOs, and communities in protecting our precious coastlines.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <Link 
              href="/register" 
              className="btn-primary text-lg py-4 px-8"
            >
              Get Started
            </Link>
            <Link 
              href="/about" 
              className="btn-secondary text-lg py-4 px-8"
            >
              Learn More
            </Link>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="grid md:grid-cols-3 gap-8 mt-16">
          <div className="card p-8">
            <div className="text-4xl mb-4">🚨</div>
            <h3 className="text-xl font-semibold mb-3 text-gray-900 dark:text-white">Real-time Monitoring</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Track coastal threats and environmental changes in real-time with advanced sensors and data analysis.
            </p>
          </div>
          
          <div className="card p-8">
            <div className="text-4xl mb-4">🤝</div>
            <h3 className="text-xl font-semibold mb-3 text-gray-900 dark:text-white">Community Engagement</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Connect with local communities, NGOs, and authorities to coordinate conservation efforts.
            </p>
          </div>
          
          <div className="card p-8">
            <div className="text-4xl mb-4">🌱</div>
            <h3 className="text-xl font-semibold mb-3 text-gray-900 dark:text-white">Mangrove Conservation</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Support mangrove restoration projects and monitor their impact on coastal protection.
            </p>
          </div>
        </div>

        {/* Stats Section */}
        <div className="mt-16 card p-8">
          <h2 className="text-2xl font-bold text-center mb-8 text-gray-900 dark:text-white">Platform Impact</h2>
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-primary mb-2">1,247</div>
              <div className="text-gray-600 dark:text-gray-300">Reports Submitted</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-green-600 mb-2">89</div>
              <div className="text-gray-600 dark:text-gray-300">Active Alerts</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-purple-600 mb-2">5,432</div>
              <div className="text-gray-600 dark:text-gray-300">Community Members</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-orange-600 mb-2">23</div>
              <div className="text-gray-600 dark:text-gray-300">Projects Completed</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
