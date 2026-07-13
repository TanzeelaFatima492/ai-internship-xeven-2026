'use client'

import { BarChart3, FileUp, MessageSquare, Download, X } from 'lucide-react'

type AdminTab = 'dashboard' | 'upload' | 'analytics' | 'threads' | 'export'

interface AdminSidebarProps {
  activeTab: AdminTab
  onSelectTab: (tab: AdminTab) => void
  sidebarOpen: boolean
  onToggleSidebar: () => void
}

const navItems = [
  {
    id: 'dashboard' as AdminTab,
    label: 'Dashboard',
    icon: BarChart3,
    description: 'Overview & stats',
  },
  {
    id: 'upload' as AdminTab,
    label: 'Upload PDF',
    icon: FileUp,
    description: 'Add documents',
  },
  {
    id: 'analytics' as AdminTab,
    label: 'Analytics',
    icon: BarChart3,
    description: 'Detailed insights',
  },
  {
    id: 'threads' as AdminTab,
    label: 'Threads',
    icon: MessageSquare,
    description: 'Conversations',
  },
  {
    id: 'export' as AdminTab,
    label: 'Export',
    icon: Download,
    description: 'Data exports',
  },
]

export default function AdminSidebar({
  activeTab,
  onSelectTab,
  sidebarOpen,
  onToggleSidebar,
}: AdminSidebarProps) {
  return (
    <>
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 lg:hidden z-30"
          onClick={onToggleSidebar}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed lg:static left-0 top-0 h-screen w-64 bg-card border-r border-border transform transition-transform duration-200 z-40 lg:translate-x-0 lg:z-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="p-6 space-y-8">
          {/* Close button for mobile */}
          <button
            onClick={onToggleSidebar}
            className="lg:hidden absolute right-4 top-4 p-2 hover:bg-muted rounded-lg transition-colors"
          >
            <X size={20} />
          </button>

          {/* Navigation */}
          <nav className="space-y-2 mt-12 lg:mt-0">
            {navItems.map((item) => {
              const isActive = activeTab === item.id
              const Icon = item.icon
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    onSelectTab(item.id)
                    if (window.innerWidth < 1024) {
                      onToggleSidebar()
                    }
                  }}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-all duration-200 flex items-start gap-3 group ${
                    isActive
                      ? 'bg-gradient-to-r from-primary/20 to-accent/20 border border-primary/50 text-primary'
                      : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                  }`}
                >
                  <Icon size={20} className="mt-0.5 flex-shrink-0" />
                  <div>
                    <div className="font-semibold text-sm">{item.label}</div>
                    <div className={`text-xs ${isActive ? 'text-primary/70' : 'text-muted-foreground'}`}>
                      {item.description}
                    </div>
                  </div>
                </button>
              )
            })}
          </nav>

          {/* Sidebar Footer */}
          <div className="border-t border-border pt-4 space-y-3">
            <p className="text-xs text-muted-foreground font-semibold">ADMIN VERSION</p>
            <div className="bg-primary/5 border border-primary/20 rounded-lg p-3">
              <p className="text-xs text-muted-foreground">
                Restaurant AI Assistant Admin Panel
              </p>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
