export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="text-4xl mr-4">ℹ️</span>
            About Coastal Alert System
          </h1>
          <p className="text-xl text-gray-600 max-w-4xl leading-relaxed">
            Protecting coastal communities through advanced threat detection and early warning systems
          </p>
        </div>

        {/* Mission Statement */}
        <div className="card mb-12 bg-gradient-to-r from-ocean-50 to-blue-50 border-ocean-200">
          <h2 className="text-2xl font-bold text-ocean-800 mb-6 flex items-center">
            <span className="text-2xl mr-3">🎯</span>
            Our Mission
          </h2>
          <p className="text-lg text-ocean-700 leading-relaxed">
            Coastal areas are vital for blue carbon storage but face increasing threats from storm surges, 
            coastal erosion, pollution, and illegal activities. Our comprehensive early warning platform 
            combines cutting-edge AI/ML technology with real-time data from physical sensors, satellite feeds, 
            and historical records to protect these critical ecosystems and the communities that depend on them.
          </p>
        </div>

        {/* Key Features */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          <div className="card text-center group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-ocean-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🛰️</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Multi-Source Data</h3>
            <p className="text-gray-600 leading-relaxed">
              Integrates data from tide gauges, weather stations, satellite imagery, 
              and historical records for comprehensive monitoring.
            </p>
          </div>

          <div className="card text-center group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🤖</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">AI-Powered Analysis</h3>
            <p className="text-gray-600 leading-relaxed">
              Advanced machine learning algorithms detect patterns, anomalies, 
              and predict emerging threats before they become critical.
            </p>
          </div>

          <div className="card text-center group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-coral-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">📱</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Instant Alerts</h3>
            <p className="text-gray-600 leading-relaxed">
              Multi-channel alert system delivers actionable warnings via SMS, 
              app notifications, and web dashboards to relevant stakeholders.
            </p>
          </div>

          <div className="card text-center group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-sand-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">👥</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Community Driven</h3>
            <p className="text-gray-600 leading-relaxed">
              Empowers local communities to contribute observations and 
              participate in coastal protection efforts.
            </p>
          </div>

          <div className="card text-center group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">📊</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Real-time Monitoring</h3>
            <p className="text-gray-600 leading-relaxed">
              Continuous monitoring of coastal conditions with live data 
              visualization and trend analysis.
            </p>
          </div>

          <div className="card text-center group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🔒</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Secure & Reliable</h3>
            <p className="text-gray-600 leading-relaxed">
              Enterprise-grade security and reliability ensure critical 
              alerts reach the right people at the right time.
            </p>
          </div>
        </div>

        {/* Target Users */}
        <div className="card mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <span className="text-2xl mr-3">👥</span>
            Who We Serve
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-gray-50 p-6 rounded-lg">
              <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                <span className="mr-2">🏛️</span>
                Government Agencies
              </h4>
              <p className="text-gray-600 text-sm">
                Disaster management departments and coastal city governments 
                for emergency response coordination.
              </p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg">
              <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                <span className="mr-2">🌱</span>
                Environmental NGOs
              </h4>
              <p className="text-gray-600 text-sm">
                Conservation organizations monitoring ecosystem health 
                and environmental protection efforts.
              </p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg">
              <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                <span className="mr-2">🎣</span>
                Fisherfolk Communities
              </h4>
              <p className="text-gray-600 text-sm">
                Local fishing communities who depend on coastal waters 
                for their livelihoods and safety.
              </p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg">
              <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                <span className="mr-2">🚨</span>
                Civil Defence Teams
              </h4>
              <p className="text-gray-600 text-sm">
                Emergency response teams coordinating disaster 
                preparedness and community safety.
              </p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg">
              <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                <span className="mr-2">🏘️</span>
                Coastal Communities
              </h4>
              <p className="text-gray-600 text-sm">
                Residents and businesses in coastal areas who need 
                timely warnings about potential threats.
              </p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg">
              <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                <span className="mr-2">🔬</span>
                Researchers
              </h4>
              <p className="text-gray-600 text-sm">
                Scientists and researchers studying coastal dynamics 
                and climate change impacts.
              </p>
            </div>
          </div>
        </div>

        {/* Technology Stack */}
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <span className="text-2xl mr-3">⚙️</span>
            Technology & Capabilities
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h4 className="font-semibold text-gray-900 mb-4">Data Sources</h4>
              <ul className="space-y-2 text-gray-700">
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-ocean-500 rounded-full mr-3"></span>
                  Tide gauges and water level sensors
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-ocean-500 rounded-full mr-3"></span>
                  Weather stations and meteorological data
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-ocean-500 rounded-full mr-3"></span>
                  Satellite imagery and remote sensing
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-ocean-500 rounded-full mr-3"></span>
                  Historical environmental records
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-ocean-500 rounded-full mr-3"></span>
                  Community observations and reports
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-4">AI Capabilities</h4>
              <ul className="space-y-2 text-gray-700">
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-emerald-500 rounded-full mr-3"></span>
                  Pattern recognition and anomaly detection
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-emerald-500 rounded-full mr-3"></span>
                  Predictive modeling for threat forecasting
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-emerald-500 rounded-full mr-3"></span>
                  Real-time data fusion and analysis
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-emerald-500 rounded-full mr-3"></span>
                  Automated alert prioritization
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-emerald-500 rounded-full mr-3"></span>
                  Trend analysis and long-term monitoring
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}