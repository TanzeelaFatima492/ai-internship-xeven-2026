'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { LogOut, ChefHat, Download } from 'lucide-react'
import AnalyticsHeader from '@/components/analytics-header'
import AnalyticsStats from '@/components/analytics-stats'
import DailyUsageChart from '@/components/daily-usage-chart'
import PopularQuestionsTable from '@/components/popular-questions-table'
import RecentQueriesList from '@/components/recent-queries-list'
import DateRangeFilter from '@/components/date-range-filter'

export default function AnalyticsPage() {
  const router = useRouter()
  const [user, setUser] = useState<{ username: string; email: string } | null>(null)
  const [loading, setLoading] = useState(true)
  const [dateRange, setDateRange] = useState({
    startDate: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), // 30 days ago
    endDate: new Date(),
  })
  const [exporting, setExporting] = useState(false)

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

  const handleExport = () => {
    setExporting(true)
    
    const analyticsData = {
      exportDate: new Date().toISOString(),
      dateRange: {
        startDate: dateRange.startDate.toISOString(),
        endDate: dateRange.endDate.toISOString(),
      },
      stats: {
        totalQueries: 342,
        totalDocuments: 12,
        activeThreads: 87,
        totalUsers: 45,
      },
      dailyUsage: [
        { date: '2024-12-01', queries: 45 },
        { date: '2024-12-02', queries: 52 },
        { date: '2024-12-03', queries: 48 },
        { date: '2024-12-04', queries: 61 },
        { date: '2024-12-05', queries: 55 },
        { date: '2024-12-06', queries: 67 },
        { date: '2024-12-07', queries: 72 },
      ],
      popularQuestions: [
        { question: "What's the biryani price?", count: 145, percentage: 42.4 },
        { question: "Do you have vegetarian options?", count: 98, percentage: 28.7 },
        { question: "What are delivery hours?", count: 67, percentage: 19.6 },
        { question: "Tell me about offers", count: 45, percentage: 13.2 },
        { question: "How to place an order?", count: 32, percentage: 9.4 },
      ],
      recentQueries: [
        {
          id: '1',
          question: "What's your cheapest item?",
          timestamp: new Date(Date.now() - 5 * 60000),
          category: 'Menu',
        },
        {
          id: '2',
          question: "Do you deliver to my area?",
          timestamp: new Date(Date.now() - 15 * 60000),
          category: 'Policies',
        },
        {
          id: '3',
          question: "Any spicy options?",
          timestamp: new Date(Date.now() - 25 * 60000),
          category: 'Dietary',
        },
        {
          id: '4',
          question: "Weekend special offers?",
          timestamp: new Date(Date.now() - 45 * 60000),
          category: 'Offers',
        },
        {
          id: '5',
          question: "Gluten-free menu available?",
          timestamp: new Date(Date.now() - 65 * 60000),
          category: 'Dietary',
        },
      ],
    }

    const dataStr = JSON.stringify(analyticsData, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `analytics-${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)

    setExporting(false)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    router.push('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background to-background/95 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading analytics...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <main className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-40">
        <div className="px-4 md:px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-primary via-accent to-secondary p-2 rounded-lg">
              <ChefHat className="w-6 h-6 text-card" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground">Analytics</h1>
              <p className="text-xs text-muted-foreground">BiteWise AI Assistant</p>
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

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="max-w-7xl mx-auto px-4 md:px-6 py-8">
          {/* Page Header */}
          <AnalyticsHeader />

          {/* Controls */}
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
            <DateRangeFilter
              dateRange={dateRange}
              onDateRangeChange={setDateRange}
            />
            <button
              onClick={handleExport}
              disabled={exporting}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-primary via-accent to-secondary text-card rounded-lg hover:shadow-lg transition-all duration-200 disabled:opacity-50 font-medium text-sm md:text-base"
            >
              <Download size={18} />
              <span>{exporting ? 'Exporting...' : 'Export as JSON'}</span>
            </button>
          </div>

          {/* Stats Cards */}
          <AnalyticsStats />

          {/* Charts and Tables */}
          <div className="grid lg:grid-cols-3 gap-6 mb-8">
            {/* Daily Usage Chart - Full Width on Mobile, 2/3 on Desktop */}
            <div className="lg:col-span-2">
              <DailyUsageChart />
            </div>

            {/* Popular Questions - 1/3 on Desktop */}
            <PopularQuestionsTable />
          </div>

          {/* Recent Queries */}
          <RecentQueriesList />
        </div>
      </div>
    </main>
  )
}
