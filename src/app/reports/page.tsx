'use client';

import { useState, useEffect } from 'react';

interface Report {
  id: string;
  type: string;
  title: string;
  description: string;
  location: string;
  submittedBy: string;
  timestamp: string;
  status: string;
}

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    type: '',
    title: '',
    description: '',
    location: ''
  });

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const response = await fetch('/api/reports');
      const data = await response.json();
      if (data.success) {
        setReports(data.reports);
      }
    } catch (error) {
      console.error('Failed to fetch reports:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/reports', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        setShowForm(false);
        setFormData({ type: '', title: '', description: '', location: '' });
        fetchReports();
      }
    } catch (error) {
      console.error('Failed to submit report:', error);
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'erosion': return '🏖️';
      case 'water_quality': return '💧';
      case 'wildlife': return '🐢';
      case 'pollution': return '🏭';
      case 'weather': return '🌪️';
      case 'accessibility': return '♿';
      default: return '📋';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-emerald-100 text-emerald-800';
      case 'pending': return 'bg-sand-100 text-sand-800';
      case 'resolved': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-ocean-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading reports...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="text-4xl mr-4">📊</span>
            Coastal Reports
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl">
            Community-driven reporting system for coastal observations, threats, and environmental changes.
          </p>
        </div>

        {/* Action Bar */}
        <div className="mb-8 flex justify-between items-center">
          <div className="flex space-x-4">
            <button className="btn-secondary">
              Filter Reports
            </button>
            <button className="btn-secondary">
              Export Data
            </button>
          </div>
          <button 
            onClick={() => setShowForm(true)}
            className="btn-primary flex items-center space-x-2"
          >
            <span>📝</span>
            <span>Create New Report</span>
          </button>
        </div>

        {/* Report Form Modal */}
        {showForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-2xl font-bold text-gray-900">Submit New Report</h2>
                <p className="text-gray-600 mt-2">Help protect our coastal environment by reporting observations</p>
              </div>
              
              <form onSubmit={handleSubmit} className="p-6 space-y-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Report Type</label>
                  <select 
                    value={formData.type}
                    onChange={(e) => setFormData({...formData, type: e.target.value})}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-ocean-500 focus:border-transparent"
                    required
                  >
                    <option value="">Select type...</option>
                    <option value="erosion">🏖️ Beach Erosion</option>
                    <option value="water_quality">💧 Water Quality</option>
                    <option value="wildlife">🐢 Wildlife Activity</option>
                    <option value="pollution">🏭 Pollution</option>
                    <option value="weather">🌪️ Weather Event</option>
                    <option value="accessibility">♿ Accessibility Issue</option>
                    <option value="other">📋 Other</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Title</label>
                  <input 
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-ocean-500 focus:border-transparent"
                    placeholder="Brief description of the issue"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Location</label>
                  <input 
                    type="text"
                    value={formData.location}
                    onChange={(e) => setFormData({...formData, location: e.target.value})}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-ocean-500 focus:border-transparent"
                    placeholder="Specific location or coordinates"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Description</label>
                  <textarea 
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    rows={4}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-ocean-500 focus:border-transparent"
                    placeholder="Detailed description of what you observed..."
                    required
                  />
                </div>

                <div className="flex space-x-4 pt-4">
                  <button 
                    type="button"
                    onClick={() => setShowForm(false)}
                    className="btn-secondary flex-1"
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit"
                    className="btn-primary flex-1"
                  >
                    Submit Report
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Reports Grid */}
        <div className="space-y-6">
          {reports.map((report) => (
            <div key={report.id} className="card hover:shadow-lg transition-all duration-200">
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-4 flex-1">
                  <div className="text-3xl">{getTypeIcon(report.type)}</div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-xl font-bold text-gray-900">{report.title}</h3>
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wide ${getStatusColor(report.status)}`}>
                        {report.status}
                      </span>
                    </div>
                    <p className="text-gray-700 mb-4 leading-relaxed">{report.description}</p>
                    <div className="flex items-center space-x-6 text-sm text-gray-600">
                      <div className="flex items-center">
                        <span className="mr-2">📍</span>
                        <span className="font-medium">{report.location}</span>
                      </div>
                      <div className="flex items-center">
                        <span className="mr-2">👤</span>
                        <span>{report.submittedBy}</span>
                      </div>
                      <div className="flex items-center">
                        <span className="mr-2">🕒</span>
                        <span>{new Date(report.timestamp).toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="flex space-x-2 ml-4">
                  <button className="btn-secondary text-sm py-2 px-4">
                    View Details
                  </button>
                  <button className="text-gray-400 hover:text-gray-600 p-2">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Report Guidelines */}
        <div className="mt-12">
          <div className="card bg-ocean-50 border-ocean-200">
            <h2 className="text-xl font-bold text-ocean-800 mb-4 flex items-center">
              <span className="mr-3">💡</span>
              Reporting Guidelines
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm text-ocean-700">
              <div>
                <h4 className="font-semibold mb-2">What to Report:</h4>
                <ul className="space-y-1">
                  <li>• Unusual coastal erosion patterns</li>
                  <li>• Water quality changes</li>
                  <li>• Wildlife behavior anomalies</li>
                  <li>• Pollution incidents</li>
                  <li>• Infrastructure damage</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-2">Best Practices:</h4>
                <ul className="space-y-1">
                  <li>• Include precise location details</li>
                  <li>• Provide clear, factual descriptions</li>
                  <li>• Add photos when possible</li>
                  <li>• Report immediately for urgent threats</li>
                  <li>• Follow up on status changes</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}