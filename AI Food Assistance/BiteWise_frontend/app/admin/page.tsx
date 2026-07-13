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
    totalDocuments: 12,
    totalQueries: 342,
    totalThreads: 87,
    activeUsers: 45,
  })
  const [sidebarOpen, setSidebarOpen] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/')
      return
    }

    try {
      const payload = JSON.parse(
        Buffer.from(token.split('.')[1], 'base64').toString()
      )
      setUser({
        username: payload.username,
        email: payload.email,
      })
    } catch (err) {
      console.error('Invalid token:', err)
      localStorage.removeItem('token')
      router.push('/')
    } finally {
      setLoading(false)
    }
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('token')
    router.push('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background to-background/95 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading admin dashboard...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-40">
        <div className="px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="lg:hidden p-2 hover:bg-muted rounded-lg transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <div>
              <h1 className="text-xl font-bold text-foreground">BiteWise Admin</h1>
              <p className="text-xs text-muted-foreground">Dashboard</p>
            </div>
          </div>

          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-3 md:px-4 py-2 bg-destructive/10 hover:bg-destructive/20 text-destructive rounded-lg transition-colors text-sm md:text-base"
          >
            <LogOut size={18} />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </header>

      {/* Main Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <AdminSidebar
          activeTab={activeTab}
          onSelectTab={setActiveTab}
          sidebarOpen={sidebarOpen}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        />

        {/* Main Content */}
        <main className="flex-1 overflow-auto">
          <div className="p-4 md:p-8">
            {/* Dashboard Tab */}
            {activeTab === 'dashboard' && (
              <div className="space-y-8">
                <div>
                  <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-2">Dashboard</h2>
                  <p className="text-muted-foreground">Monitor your restaurant AI system performance</p>
                </div>

                {/* Stats Cards */}
                <StatsCards stats={stats} />

                {/* Charts and Tables */}
                <div className="grid lg:grid-cols-2 gap-6">
                  <RecentQuestionsTable />
                  <PopularQuestionsChart />
                </div>
              </div>
            )}

            {/* Upload Tab */}
            {activeTab === 'upload' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-2">Upload Documents</h2>
                  <p className="text-muted-foreground">Add menu PDFs and restaurant information</p>
                </div>
                <PDFUploadArea onUploadComplete={() => {
                  setStats(prev => ({
                    ...prev,
                    totalDocuments: prev.totalDocuments + 1
                  }))
                }} />
              </div>
            )}

            {/* Analytics Tab */}
            {activeTab === 'analytics' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-2">Analytics</h2>
                  <p className="text-muted-foreground">Detailed insights and metrics</p>
                </div>
                <div className="bg-card border border-border rounded-xl p-6">
                  <div className="text-center py-12">
                    <BarChart3 className="w-12 h-12 text-primary mx-auto mb-4 opacity-50" />
                    <p className="text-muted-foreground">Analytics data will be displayed here</p>
                  </div>
                </div>
              </div>
            )}

            {/* Threads Tab */}
            {activeTab === 'threads' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-2">Conversation Threads</h2>
                  <p className="text-muted-foreground">View all user conversations</p>
                </div>
                <div className="bg-card border border-border rounded-xl p-6">
                  <div className="text-center py-12">
                    <MessageSquare className="w-12 h-12 text-accent mx-auto mb-4 opacity-50" />
                    <p className="text-muted-foreground">Thread management will be displayed here</p>
                  </div>
                </div>
              </div>
            )}

            {/* Export Tab */}
            {activeTab === 'export' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-2">Export Data</h2>
                  <p className="text-muted-foreground">Download reports and data exports</p>
                </div>
                <div className="grid md:grid-cols-3 gap-4">
                  {[
                    { title: 'Query Report', desc: 'All user queries and AI responses', icon: MessageSquare },
                    { title: 'User Analytics', desc: 'User engagement and metrics', icon: BarChart3 },
                    { title: 'Document List', desc: 'All uploaded documents', icon: FileUp },
                  ].map((item, i) => (
                    <button
                      key={i}
                      className="bg-card border border-border rounded-xl p-6 hover:border-primary/50 transition-colors text-left group"
                    >
                      <div className="flex items-start justify-between mb-4">
                        <item.icon className="w-8 h-8 text-primary" />
                        <Download className="w-5 h-5 text-muted-foreground group-hover:text-primary transition-colors" />
                      </div>
                      <h3 className="font-semibold text-foreground mb-1">{item.title}</h3>
                      <p className="text-sm text-muted-foreground">{item.desc}</p>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}
