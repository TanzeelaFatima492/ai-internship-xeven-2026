'use client'

import { BarChart3, FileUp, MessageSquare, Download, X, ChefHat } from 'lucide-react'

type AdminTab = 'dashboard' | 'upload' | 'analytics' | 'threads' | 'export'

interface AdminSidebarProps {
  activeTab: AdminTab
  onSelectTab: (tab: AdminTab) => void
  sidebarOpen: boolean
  onToggleSidebar: () => void
}

const navItems = [
  { id: 'dashboard' as AdminTab, label: 'Dashboard', icon: BarChart3, description: 'Overview & stats' },
  { id: 'upload' as AdminTab, label: 'Upload PDF', icon: FileUp, description: 'Add documents' },
  { id: 'analytics' as AdminTab, label: 'Analytics', icon: BarChart3, description: 'Detailed insights' },
  { id: 'threads' as AdminTab, label: 'Threads', icon: MessageSquare, description: 'Conversations' },
  { id: 'export' as AdminTab, label: 'Export', icon: Download, description: 'Data exports' },
]

export default function AdminSidebar({ activeTab, onSelectTab, sidebarOpen, onToggleSidebar }: AdminSidebarProps) {
  return (
    <>
      {sidebarOpen && <div className="fixed inset-0 bg-black/50 lg:hidden z-30" onClick={onToggleSidebar} />}

      <aside className={`fixed lg:static left-0 top-0 h-screen w-64 bg-gray-900 border-r border-gray-800 transform transition-transform duration-200 z-40 lg:translate-x-0 lg:z-0 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="p-6 space-y-8">
          <button onClick={onToggleSidebar} className="lg:hidden absolute right-4 top-4 p-2 hover:bg-gray-800 rounded-lg text-white">
            <X size={20} />
          </button>

          {/* Logo */}
          <div className="flex items-center gap-3 mt-4 lg:mt-0">
            <div className="bg-gradient-to-br from-orange-500 to-orange-600 p-2 rounded-lg">
              <ChefHat className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">BiteWise</h2>
              <p className="text-xs text-gray-400">Admin Panel</p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="space-y-1">
            {navItems.map((item) => {
              const isActive = activeTab === item.id
              const Icon = item.icon
              return (
                <button
                  key={item.id}
                  onClick={() => { onSelectTab(item.id); if (window.innerWidth < 1024) onToggleSidebar() }}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-all duration-200 flex items-center gap-3 ${
                    isActive
                      ? 'bg-orange-500/10 border border-orange-500/50 text-orange-400'
                      : 'text-gray-400 hover:text-white hover:bg-gray-800'
                  }`}
                >
                  <Icon size={20} />
                  <div>
                    <div className="font-semibold text-sm">{item.label}</div>
                    <div className="text-xs opacity-70">{item.description}</div>
                  </div>
                </button>
              )
            })}
          </nav>

          {/* Footer */}
          <div className="border-t border-gray-800 pt-4">
            <p className="text-xs text-gray-500 font-semibold mb-3">Delicious Food, Smartly Delivered</p>
            <div className="bg-orange-500/5 border border-orange-500/20 rounded-lg p-3">
              <p className="text-xs text-gray-400">Restaurant AI Assistant</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}