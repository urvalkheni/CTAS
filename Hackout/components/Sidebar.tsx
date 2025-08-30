'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState } from 'react'

interface SidebarProps {
  userRole?: string
}

export default function Sidebar({ userRole = 'community' }: SidebarProps) {
  const pathname = usePathname()
  const [isCollapsed, setIsCollapsed] = useState(false)

  const navigationItems = [
    {
      name: 'Dashboard',
      href: '/dashboard',
      icon: '📊',
      roles: ['authority', 'ngo', 'community']
    },
    {
      name: 'Alerts',
      href: '/alerts',
      icon: '🚨',
      roles: ['authority', 'ngo', 'community']
    },
    {
      name: 'Reports',
      href: '/reports',
      icon: '📝',
      roles: ['authority', 'ngo', 'community']
    },
    {
      name: 'Leaderboard',
      href: '/leaderboard',
      icon: '🏆',
      roles: ['authority', 'ngo', 'community']
    },
    {
      name: 'Trends',
      href: '/trends',
      icon: '📈',
      roles: ['authority', 'ngo', 'community']
    },
    {
      name: 'Settings',
      href: '/settings',
      icon: '⚙️',
      roles: ['authority', 'ngo', 'community']
    }
  ]

  const filteredItems = navigationItems.filter(item => 
    item.roles.includes(userRole)
  )

  return (
    <div className={`bg-white shadow-lg h-screen transition-all duration-300 ${
      isCollapsed ? 'w-16' : 'w-64'
    }`}>
      <div className="p-4 border-b">
        <div className="flex items-center justify-between">
          {!isCollapsed && (
            <h2 className="text-xl font-bold text-gray-800">
              Coastal Platform
            </h2>
          )}
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-2 rounded-lg hover:bg-gray-100"
          >
            {isCollapsed ? '→' : '←'}
          </button>
        </div>
      </div>

      <nav className="mt-6">
        <div className="px-3">
          {filteredItems.map((item) => {
            const isActive = pathname === item.href
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center px-3 py-3 mb-2 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-blue-100 text-blue-700 border-r-2 border-blue-700'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <span className="text-xl mr-3">{item.icon}</span>
                {!isCollapsed && (
                  <span className="font-medium">{item.name}</span>
                )}
              </Link>
            )
          })}
        </div>
      </nav>

      <div className="absolute bottom-4 left-4 right-4">
        <div className="bg-gray-50 rounded-lg p-3">
          {!isCollapsed && (
            <div className="text-sm text-gray-600 mb-2">
              Role: <span className="font-medium capitalize">{userRole}</span>
            </div>
          )}
          <Link
            href="/"
            className="flex items-center text-gray-600 hover:text-gray-900"
          >
            <span className="text-lg mr-2">🏠</span>
            {!isCollapsed && <span>Home</span>}
          </Link>
        </div>
      </div>
    </div>
  )
}
