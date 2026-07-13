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

const StatCard = ({
  title,
  value,
  icon: Icon,
  trend,
  color,
}: {
  title: string
  value: number
  icon: React.ReactNode
  trend?: string
  color: string
}) => (
  <div className="bg-card border border-border rounded-xl p-6 hover:border-primary/50 transition-all duration-200 group">
    <div className="flex items-start justify-between mb-4">
      <div className={`p-3 rounded-lg ${color}`}>{Icon}</div>
      {trend && (
        <span className="text-xs font-semibold text-green-500 bg-green-500/10 px-2 py-1 rounded">
          {trend}
        </span>
      )}
    </div>
    <h3 className="text-muted-foreground text-sm font-medium mb-2">{title}</h3>
    <div className="flex items-end justify-between">
      <div className="text-3xl md:text-4xl font-bold text-foreground">{value}</div>
    </div>
  </div>
)

export default function StatsCards({ stats }: StatsCardsProps) {
  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatCard
        title="Total Documents"
        value={stats.totalDocuments}
        icon={<FileText className="w-6 h-6 text-card" />}
        trend="+2 this week"
        color="bg-gradient-to-br from-primary/20 to-primary/10"
      />
      <StatCard
        title="Total Queries"
        value={stats.totalQueries}
        icon={<MessageCircle className="w-6 h-6 text-card" />}
        trend="+48 today"
        color="bg-gradient-to-br from-accent/20 to-accent/10"
      />
      <StatCard
        title="Conversation Threads"
        value={stats.totalThreads}
        icon={<BarChart3 className="w-6 h-6 text-card" />}
        trend="+12 this week"
        color="bg-gradient-to-br from-secondary/20 to-secondary/10"
      />
      <StatCard
        title="Active Users"
        value={stats.activeUsers}
        icon={<Users className="w-6 h-6 text-card" />}
        trend="+8 new users"
        color="bg-gradient-to-br from-primary/20 via-accent/20 to-secondary/10"
      />
    </div>
  )
}
