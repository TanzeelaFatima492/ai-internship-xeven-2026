'use client'

import { useEffect, useState } from 'react'

interface Thread {
  thread_id: string
}

export default function ThreadList() {
  const [threads, setThreads] = useState<Thread[]>([])

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    fetch('http://localhost:8000/rag/threads', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(r => r.json())
    .then(data => setThreads(Array.isArray(data) ? data : []))
    .catch(console.error)
  }, [])

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6">
      {threads.length === 0 ? (
        <p className="text-gray-400 text-center py-4">No threads yet</p>
      ) : (
        <div className="space-y-2">
          {threads.map((t, i) => (
            <div key={i} className="p-3 bg-gray-50 rounded-lg">
              <p className="font-medium text-gray-900">{t.thread_id}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}