'use client'

import { useState, useEffect } from 'react'
import Layout from '@/components/Layout'
import Link from 'next/link'

export default function Dashboard() {
  const [userRole, setUserRole] = useState('community')
  const [stats, setStats] = useState({
    alerts: 5,
    reports: 12,
    projects: 8,
    members: 1247
  })

  // Simulate role-based data fetching
  useEffect(() => {
    // TODO: Fetch user role from session/auth
    // For now, using mock data
  }, [])

  const AuthorityDashboard = () => (
    <div className="space-y-6">
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Active Alerts</h3>
          <p className="text-3xl font-bold text-red-600">{stats.alerts}</p>
          <p className="text-sm text-gray-500">Require attention</p>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Reports Today</h3>
          <p className="text-3xl font-bold text-blue-600">{stats.reports}</p>
          <p className="text-sm text-gray-500">Community reports</p>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Active Projects</h3>
          <p className="text-3xl font-bold text-green-600">{stats.projects}</p>
          <p className="text-sm text-gray-500">Ongoing initiatives</p>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Community Members</h3>
          <p className="text-3xl font-bold text-purple-600">{stats.members}</p>
          <p className="text-sm text-gray-500">Active users</p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4">Map Overview</h3>
          <div className="bg-gray-100 rounded-lg h-64 flex items-center justify-center">
            <p className="text-gray-500">🌍 Interactive Map Coming Soon</p>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4">Recent Alerts</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
              <div>
                <p className="font-medium text-red-800">High Tide Warning</p>
                <p className="text-sm text-red-600">Mumbai Coast</p>
              </div>
              <span className="text-xs text-red-600">2h ago</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
              <div>
                <p className="font-medium text-yellow-800">Storm Watch</p>
                <p className="text-sm text-yellow-600">Goa Coast</p>
              </div>
              <span className="text-xs text-yellow-600">4h ago</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )

  const CommunityDashboard = () => (
    <div className="space-y-6">
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Your Points</h3>
          <p className="text-3xl font-bold text-blue-600">1,250</p>
          <p className="text-sm text-gray-500">Rank #5</p>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Reports Submitted</h3>
          <p className="text-3xl font-bold text-green-600">45</p>
          <p className="text-sm text-gray-500">This month</p>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Alerts Created</h3>
          <p className="text-3xl font-bold text-orange-600">12</p>
          <p className="text-sm text-gray-500">Total</p>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Achievements</h3>
          <p className="text-3xl font-bold text-purple-600">8</p>
          <p className="text-sm text-gray-500">Badges earned</p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4">Submit Report</h3>
          <p className="text-gray-600 mb-4">
            Help protect our coastlines by reporting environmental issues or observations.
          </p>
          <Link 
            href="/reports" 
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
          >
            Create Report
          </Link>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4">Gamification</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Level Progress</span>
              <span className="text-sm font-medium">75%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-blue-600 h-2 rounded-full" style={{ width: '75%' }}></div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Next Level</span>
              <span className="text-sm font-medium">250 points needed</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )

  return (
    <Layout userRole={userRole}>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-600">Welcome back! Here's what's happening today.</p>
          </div>
          <div className="flex space-x-3">
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors">
              Create Alert
            </button>
            <button className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors">
              Submit Report
            </button>
          </div>
        </div>

        {userRole === 'authority' ? <AuthorityDashboard /> : <CommunityDashboard />}
      </div>
    </Layout>
  )
}
