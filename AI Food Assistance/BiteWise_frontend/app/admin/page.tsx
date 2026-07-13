'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { LogOut, BarChart3, FileUp, MessageSquare, Download } from 'lucide-react'
import AdminSidebar from '@/components/admin-sidebar'
import StatsCards from '@/components/stats-cards'
import RecentQuestionsTable from '@/components/recent-questions-table'
import PopularQuestionsChart from '@/components/popular-questions-chart'
import PDFUploadArea from '@/components/pdf-upload-area'

type AdminTab = 'dashboard' | 'upload' | 'analytics' | 'threads' | 'export'

interface AdminStats {
  totalDocuments: number
  totalQueries: number
  totalThreads: number
  activeUsers: number
}

export default function AdminPage() {
  const router = useRouter()
  const [user, setUser] = useState<{ username: string; email: string } | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<AdminTab>('dashboard')
  const [stats, setStats] = useState<AdminStats>({
    totalDocuments: 0,
    totalQueries: 0,
    totalThreads: 0,
    activeUsers: 0,
  })

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    if (!token) {
      router.push('/')
      return
    }
    setUser({ username: 'admin', email: 'admin@bitewise.com' })

    // Fetch real stats
    fetch('http://localhost:8000/analytics/overview', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(r => r.json())
    .then(data => setStats({
      totalDocuments: data.total_documents || 0,
      totalQueries: data.total_queries || 0,
      totalThreads: data.total_threads || 0,
      activeUsers: data.total_queries || 0,
    }))
    .catch(console.error)
    .finally(() => setLoading(false))
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('bitewise_auth_token')
    router.push('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* FIXED SIDEBAR */}
      <div className="w-64 flex-shrink-0 h-screen sticky top-0">
        <AdminSidebar
          activeTab={activeTab}
          onSelectTab={setActiveTab}
          sidebarOpen={true}
          onToggleSidebar={() => {}}
        />
      </div>

      {/* MAIN CONTENT */}
      <div className="flex-1 flex flex-col min-h-screen">
        {/* Header */}
        <header className="bg-gray-900 border-b border-gray-700 sticky top-0 z-30 px-6 py-4 flex items-center justify-between text-white">
           <div>
            <h1 className="text-xl font-bold">BiteWise Admin</h1>
            <p className="text-xs text-gray-500">Manage your restaurant AI system</p>
          </div>
          <button onClick={handleLogout} className="flex items-center gap-2 px-4 py-2 bg-red-50 text-red-600 rounded-lg">
            <LogOut size={18} /> Logout
          </button>
        </header>

        {/* Content Area */}
        <main className="flex-1 p-6 overflow-auto">
          {activeTab === 'dashboard' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold">Dashboard</h2>
              <StatsCards stats={stats} />
              <div className="grid lg:grid-cols-2 gap-6">
                <RecentQuestionsTable />
                <PopularQuestionsChart />
              </div>
            </div>
          )}

          {activeTab === 'upload' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold">Upload Documents</h2>
              <PDFUploadArea onUploadComplete={() => {
                setStats(prev => ({ ...prev, totalDocuments: prev.totalDocuments + 1 }))
              }} />
            </div>
          )}

          {activeTab === 'analytics' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold">Analytics</h2>
              <p className="text-gray-500">Real analytics data loading...</p>
            </div>
          )}

          {activeTab === 'threads' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold">Conversation Threads</h2>
              <p className="text-gray-500">Real threads loading...</p>
            </div>
          )}

          {activeTab === 'export' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold">Export Data</h2>
              <div className="grid md:grid-cols-3 gap-4">
                {['Query Report', 'User Analytics', 'Document List'].map((item, i) => (
                  <button key={i} className="bg-white border rounded-xl p-6 hover:border-orange-500 transition-colors text-left">
                    <Download className="w-8 h-8 text-orange-500 mb-4" />
                    <h3 className="font-semibold">{item}</h3>
                    <p className="text-sm text-gray-500">Download as JSON</p>
                  </button>
                ))}
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}