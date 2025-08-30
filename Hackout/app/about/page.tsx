export default function About() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">
            About Coastal Protection Platform
          </h1>
          
          <div className="bg-white rounded-lg shadow-md p-8 mb-8">
            <h2 className="text-2xl font-semibold mb-4">Our Mission</h2>
            <p className="text-gray-600 mb-6">
              We are dedicated to protecting coastal ecosystems through real-time monitoring, 
              community engagement, and data-driven conservation strategies. Our platform 
              connects stakeholders across the globe to safeguard our precious coastlines.
            </p>
            
            <h2 className="text-2xl font-semibold mb-4">What We Do</h2>
            <ul className="list-disc list-inside text-gray-600 space-y-2 mb-6">
              <li>Real-time coastal threat monitoring and alerting</li>
              <li>Community-driven mangrove conservation initiatives</li>
              <li>Data analysis and environmental reporting</li>
              <li>Stakeholder coordination and communication</li>
              <li>Educational resources and awareness campaigns</li>
            </ul>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold mb-3">Technology</h3>
              <p className="text-gray-600">
                Built with modern web technologies including Next.js, React, TypeScript, 
                and MongoDB for robust, scalable performance.
              </p>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold mb-3">Community</h3>
              <p className="text-gray-600">
                Join thousands of environmentalists, researchers, and community leaders 
                working together to protect our coastlines.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
