'use client'

import Sidebar from './Sidebar'

interface LayoutProps {
  children: React.ReactNode
  userRole?: string
}

export default function Layout({ children, userRole = 'community' }: LayoutProps) {
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar userRole={userRole} />
      <main className="flex-1 overflow-auto">
        <div className="p-6">
          {children}
        </div>
      </main>
    </div>
  )
}
