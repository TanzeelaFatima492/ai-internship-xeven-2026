'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { LogOut, ChefHat, Download } from 'lucide-react'

interface AnalyticsData {
  overview: { total_queries: number; total_documents: number; total_chunks: number; total_threads: number }
  popularQuestions: { question: string; count: number }[]
  dailyUsage: { date: string; queries: number }[]
  recentQueries: { id: number; question: string; answer: string; created_at: string }[]
}

export default function AnalyticsPage() {
  const router = useRouter()
  const [user, setUser] = useState<{ username: string } | null>(null)
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState<AnalyticsData | null>(null)

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    if (!token) { router.push('/'); return }
    setUser({ username: 'admin' })

    Promise.all([
      fetch('http://localhost:8000/analytics/overview', { headers: { Authorization: `Bearer ${token}` } }),
      fetch('http://localhost:8000/analytics/popular-questions?limit=10', { headers: { Authorization: `Bearer ${token}` } }),
      fetch('http://localhost:8000/analytics/daily-usage', { headers: { Authorization: `Bearer ${token}` } }),
      fetch('http://localhost:8000/analytics/recent-queries?limit=10', { headers: { Authorization: `Bearer ${token}` } }),
    ])
      .then(responses => Promise.all(responses.map(r => r.json())))
      .then(([overview, popularQuestions, dailyUsage, recentQueries]) => {
        setData({ overview, popularQuestions, dailyUsage, recentQueries })
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [router])

  const handleExport = () => {
    if (!data) return
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `bitewise-analytics-${new Date().toISOString().split('T')[0]}.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  if (loading) return <div className="min-h-screen flex items-center justify-center"><div className="animate-spin h-12 w-12 border-b-2 border-orange-500 rounded-full"></div></div>

  return (
    <main className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-gradient-to-br from-orange-500 to-orange-600 p-2 rounded-lg">
            <ChefHat className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-xl font-bold text-gray-900">Analytics</h1>
        </div>
        <button onClick={() => { localStorage.removeItem('bitewise_auth_token'); router.push('/') }}
          className="flex items-center gap-2 px-4 py-2 bg-red-50 text-red-600 rounded-lg">
          <LogOut size={18} /> Logout
        </button>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Export */}
        <div className="flex justify-end mb-6">
          <button onClick={handleExport} className="flex items-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600">
            <Download size={18} /> Export JSON
          </button>
        </div>

        {data && (
          <div className="space-y-6">
            {/* Stats */}
            <div className="grid grid-cols-4 gap-4">
              {[
                { label: 'Total Queries', value: data.overview.total_queries },
                { label: 'Documents', value: data.overview.total_documents },
                { label: 'Chunks', value: data.overview.total_chunks },
                { label: 'Threads', value: data.overview.total_threads },
              ].map((s, i) => (
                <div key={i} className="bg-white rounded-xl border border-gray-200 p-4">
                  <p className="text-sm text-gray-500">{s.label}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-1">{s.value}</p>
                </div>
              ))}
            </div>

            {/* Popular Questions */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Popular Questions</h3>
              {data.popularQuestions.slice(0, 5).map((q, i) => (
                <div key={i} className="flex justify-between py-2 border-b border-gray-100 last:border-0">
                  <span className="text-gray-700">{q.question}</span>
                  <span className="bg-orange-100 text-orange-700 px-3 py-1 rounded-full text-sm">{q.count}x</span>
                </div>
              ))}
            </div>

            {/* Recent Queries */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Queries</h3>
              {data.recentQueries.slice(0, 5).map((q) => (
                <div key={q.id} className="p-3 bg-gray-50 rounded-lg mb-2">
                  <p className="font-medium text-gray-900">Q: {q.question}</p>
                  <p className="text-sm text-gray-500 mt-1">A: {q.answer?.substring(0, 100)}...</p>
                  <p className="text-xs text-gray-400 mt-1">{new Date(q.created_at).toLocaleString()}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  )
}