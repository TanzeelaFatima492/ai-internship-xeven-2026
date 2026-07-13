'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { LogOut, Download } from 'lucide-react'
import AdminSidebar from '@/components/admin-sidebar'
import StatsCards from '@/components/stats-cards'
import RecentQuestionsTable from '@/components/recent-questions-table'
import PopularQuestionsChart from '@/components/popular-questions-chart'
import PDFUploadArea from '@/components/pdf-upload-area'
import AnalyticsDashboard from '@/components/analytics-dashboard'
import ThreadList from '@/components/thread-list'

type AdminTab = 'dashboard' | 'upload' | 'analytics' | 'threads' | 'export'

interface AdminStats {
  totalDocuments: number
  totalQueries: number
  totalThreads: number
  activeUsers: number
}

export default function AdminPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<AdminTab>('dashboard')
  const [stats, setStats] = useState<AdminStats>({
    totalDocuments: 0, totalQueries: 0, totalThreads: 0, activeUsers: 0,
  })

  const downloadJSON = async (endpoint: string, filename: string) => {
    const token = localStorage.getItem('bitewise_auth_token')
    try {
      const res = await fetch(`http://localhost:8000/${endpoint}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      const data = await res.json()
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${filename}-${new Date().toISOString().split('T')[0]}.json`
      a.click()
      URL.revokeObjectURL(url)
    } catch { alert('Download failed.') }
  }

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    const role = localStorage.getItem('user_role')
    if (!token) { router.push('/'); return }
    if (role !== 'admin') { router.push('/home'); return }

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
    localStorage.removeItem('user_role')
    router.push('/')
  }

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="animate-spin h-12 w-12 border-b-2 border-orange-500 rounded-full"></div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-50 flex">
      <div className="w-64 flex-shrink-0 h-screen sticky top-0">
        <AdminSidebar activeTab={activeTab} onSelectTab={setActiveTab} sidebarOpen={true} onToggleSidebar={() => {}} />
      </div>
      <div className="flex-1 flex flex-col min-h-screen">
        <header className="bg-white border-b border-gray-200 sticky top-0 z-30 px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900">BiteWise Admin</h1>
            <p className="text-xs text-gray-500">Manage your restaurant AI system</p>
          </div>
          <button onClick={handleLogout} className="flex items-center gap-2 px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100">
            <LogOut size={18} /> Logout
          </button>
        </header>

        <main className="flex-1 p-6 overflow-auto">
          {activeTab === 'dashboard' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
              <StatsCards stats={stats} />
              <div className="grid lg:grid-cols-2 gap-6">
                <RecentQuestionsTable />
                <PopularQuestionsChart />
              </div>
            </div>
          )}

          {activeTab === 'upload' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-900">Upload Documents</h2>
              <PDFUploadArea onUploadComplete={() => setStats(prev => ({ ...prev, totalDocuments: prev.totalDocuments + 1 }))} />
            </div>
          )}

          {activeTab === 'analytics' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-900">Analytics</h2>
              <AnalyticsDashboard />
            </div>
          )}

          {activeTab === 'threads' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-900">Conversation Threads</h2>
              <ThreadList />
            </div>
          )}

          {activeTab === 'export' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-900">Export Data</h2>
              <div className="grid md:grid-cols-3 gap-4">
                {[
                  { label: 'Overview Report', desc: 'System stats', endpoint: 'analytics/overview', file: 'bitewise-overview' },
                  { label: 'Popular Questions', desc: 'User queries', endpoint: 'analytics/popular-questions?limit=50', file: 'bitewise-questions' },
                  { label: 'Thread List', desc: 'Conversations', endpoint: 'rag/threads', file: 'bitewise-threads' },
                ].map((item, i) => (
                  <button key={i} onClick={() => downloadJSON(item.endpoint, item.file)}
                    className="bg-white border border-gray-200 rounded-xl p-6 hover:border-orange-300 transition-colors text-left">
                    <Download className="w-8 h-8 text-orange-500 mb-4" />
                    <h3 className="font-semibold text-gray-900">{item.label}</h3>
                    <p className="text-sm text-gray-500">{item.desc}</p>
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