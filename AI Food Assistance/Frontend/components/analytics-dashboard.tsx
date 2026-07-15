'use client'
import { useEffect, useState } from 'react'

export default function AnalyticsDashboard() {
  const [data, setData] = useState<any>(null)
  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    Promise.all([
      fetch('http://localhost:8000/analytics/overview', { headers: { Authorization: `Bearer ${token}` } }),
      fetch('http://localhost:8000/analytics/popular-questions?limit=10', { headers: { Authorization: `Bearer ${token}` } }),
      fetch('http://localhost:8000/analytics/daily-usage', { headers: { Authorization: `Bearer ${token}` } }),
      fetch('http://localhost:8000/analytics/recent-queries?limit=10', { headers: { Authorization: `Bearer ${token}` } }),
    ]).then(rs => Promise.all(rs.map(r => r.json()))).then(([o, p, d, r]) => setData({ overview: o, popularQuestions: p, dailyUsage: d, recentQueries: r })).catch(console.error)
  }, [])
  if (!data) return <p className='text-gray-400'>Loading analytics...</p>
  return (
    <div className='space-y-6'>
      <div className='grid grid-cols-4 gap-4'>
        {[{l:'Queries',v:data.overview.total_queries},{l:'Documents',v:data.overview.total_documents},{l:'Chunks',v:data.overview.total_chunks},{l:'Threads',v:data.overview.total_threads}].map((s,i)=>(<div key={i} className='bg-white rounded-xl border p-4'><p className='text-sm text-gray-500'>{s.l}</p><p className='text-3xl font-bold'>{s.v}</p></div>))}
      </div>
      <div className='bg-white rounded-xl border p-6'><h3 className='font-semibold mb-4'>Popular Questions</h3>{data.popularQuestions.slice(0,5).map((q:any,i:number)=>(<div key={i} className='flex justify-between py-2 border-b'><span>{q.question}</span><span className='bg-orange-100 px-3 rounded-full text-sm'>{q.count}x</span></div>))}</div>
      <div className='bg-white rounded-xl border p-6'><h3 className='font-semibold mb-4'>Recent Queries</h3>{data.recentQueries.slice(0,5).map((q:any)=>(<div key={q.id} className='p-3 bg-gray-50 rounded-lg mb-2'><p className='font-medium'>Q: {q.question}</p><p className='text-sm text-gray-500'>A: {q.answer?.substring(0,80)}...</p></div>))}</div>
    </div>
  )
}