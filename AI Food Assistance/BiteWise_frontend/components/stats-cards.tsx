'use client'

import { FileText, MessageCircle, Users, BarChart3 } from 'lucide-react'

interface StatsCardsProps {
  stats: {
    totalDocuments: number
    totalQueries: number
    totalThreads: number
    activeUsers: number
  }
}

export default function StatsCards({ stats }: StatsCardsProps) {
  const cards = [
    { title: 'Total Documents', value: stats.totalDocuments, icon: FileText, color: 'bg-orange-50 text-orange-600' },
    { title: 'Total Queries', value: stats.totalQueries, icon: MessageCircle, color: 'bg-green-50 text-green-600' },
    { title: 'Threads', value: stats.totalThreads, icon: BarChart3, color: 'bg-purple-50 text-purple-600' },
    { title: 'Active Users', value: stats.activeUsers, icon: Users, color: 'bg-blue-50 text-blue-600' },
  ]

  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, i) => (
        <div key={i} className="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-md transition-all">
          <div className={`p-3 rounded-lg inline-block ${card.color} mb-4`}>
            <card.icon size={24} />
          </div>
          <h3 className="text-sm text-gray-500 font-medium">{card.title}</h3>
          <p className="text-3xl font-bold text-gray-900 mt-1">{card.value}</p>
        </div>
      ))}
    </div>
  )
}