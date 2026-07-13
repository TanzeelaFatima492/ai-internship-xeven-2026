'use client'

import { useEffect, useState } from 'react'

interface Question {
  question: string
  count: number
}

export default function PopularQuestionsTable() {
  const [questions, setQuestions] = useState<Question[]>([])
  const maxCount = questions[0]?.count || 1

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    fetch('http://localhost:8000/analytics/popular-questions?limit=5', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(r => r.json())
    .then(data => setQuestions(data))
    .catch(console.error)
  }, [])

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6">
      <h3 className="text-lg font-bold text-gray-900 mb-4">Popular Questions</h3>
      {questions.length === 0 ? (
        <p className="text-gray-400 text-center py-4">No data yet</p>
      ) : (
        <div className="space-y-3">
          {questions.map((q, i) => {
            const pct = Math.round((q.count / maxCount) * 100)
            return (
              <div key={i} className="p-3 bg-gray-50 rounded-lg">
                <div className="flex justify-between mb-1">
                  <p className="text-sm font-medium text-gray-700">{q.question}</p>
                  <span className="text-xs font-semibold text-orange-600 bg-orange-50 px-2 py-0.5 rounded-full">{q.count}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="h-full bg-orange-500 rounded-full" style={{ width: `${pct}%` }} />
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}