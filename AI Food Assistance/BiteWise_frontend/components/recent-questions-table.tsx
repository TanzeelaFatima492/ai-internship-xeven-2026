'use client'

import { useEffect, useState } from 'react'

interface Question {
  id: number
  question: string
  answer: string
  created_at: string
}

export default function RecentQuestionsTable() {
  const [questions, setQuestions] = useState<Question[]>([])

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
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div className="p-6 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Recent Questions</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left font-semibold text-gray-600">Question</th>
              <th className="px-6 py-3 text-left font-semibold text-gray-600">Answer</th>
              <th className="px-6 py-3 text-left font-semibold text-gray-600">Time</th>
            </tr>
          </thead>
          <tbody>
            {questions.length === 0 ? (
              <tr>
                <td colSpan={3} className="px-6 py-8 text-center text-gray-400">No queries yet</td>
              </tr>
            ) : (
              questions.map((q) => (
                <tr key={q.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="px-6 py-4 text-gray-900 max-w-xs truncate">{q.question}</td>
                  <td className="px-6 py-4 text-gray-500 max-w-xs truncate">{q.answer?.substring(0, 60)}...</td>
                  <td className="px-6 py-4 text-gray-400 whitespace-nowrap">
                    {new Date(q.created_at).toLocaleString()}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}