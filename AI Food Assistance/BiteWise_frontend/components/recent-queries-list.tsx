'use client'

import { useEffect, useState } from 'react'
import { Clock } from 'lucide-react'

interface Query {
  id: number
  question: string
  answer: string
  created_at: string
}

export default function RecentQueriesList() {
  const [queries, setQueries] = useState<Query[]>([])

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    fetch('http://localhost:8000/analytics/recent-queries?limit=5', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(r => r.json())
    .then(data => setQuestions(data))
    .catch(console.error)
  }, [])

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6">
      <h3 className="text-lg font-bold text-gray-900 mb-4">Recent Queries</h3>
      {queries.length === 0 ? (
        <p className="text-gray-400 text-center py-4">No queries yet</p>
      ) : (
        <div className="space-y-3">
          {queries.map((q) => (
            <div key={q.id} className="p-3 bg-gray-50 rounded-lg">
              <p className="font-medium text-gray-900">Q: {q.question}</p>
              <p className="text-sm text-gray-500 mt-1">A: {q.answer?.substring(0, 80)}...</p>
              <div className="flex items-center gap-1 text-xs text-gray-400 mt-1">
                <Clock size={12} />
                {new Date(q.created_at).toLocaleString()}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}