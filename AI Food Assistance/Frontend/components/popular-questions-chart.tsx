'use client'

import { useEffect, useState } from 'react'

interface PopularQuestion {
  question: string
  count: number
}

export default function PopularQuestionsChart() {
  const [questions, setQuestions] = useState<PopularQuestion[]>([])
  const maxCount = questions[0]?.count || 1

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    fetch('http://localhost:8000/analytics/popular-questions?limit=7', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(r => r.json())
    .then(data => setQuestions(data))
    .catch(console.error)
  }, [])

  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div className="p-6 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Popular Questions</h3>
      </div>
      <div className="p-6 space-y-4">
        {questions.length === 0 ? (
          <p className="text-gray-400 text-center py-4">No data yet</p>
        ) : (
          questions.map((item, idx) => {
            const pct = Math.round((item.count / maxCount) * 100)
            return (
              <div key={idx} className="space-y-1">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-700 truncate">{item.question}</span>
                  <span className="text-gray-500 font-semibold">{item.count}</span>
                </div>
                <div className="w-full h-2 bg-gray-100 rounded-full">
                  <div className="h-full bg-orange-500 rounded-full" style={{ width: `${pct}%` }} />
                </div>
              </div>
            )
          })
        )}
      </div>
    </div>
  )
}