import { TrendingUp } from 'lucide-react'

export default function AnalyticsHeader() {
  return (
    <div className="mb-8">
      <div className="bg-gradient-to-r from-orange-500/10 via-orange-400/5 to-gray-800 border border-gray-700 rounded-2xl p-6 md:p-8">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg">
            <TrendingUp className="w-6 h-6 text-white" />
          </div>
          <div className="flex-1">
            <h2 className="text-2xl md:text-3xl font-bold text-white mb-2">
              Performance Analytics
            </h2>
            <p className="text-gray-400">
              Track user engagement, popular queries, and system performance metrics
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}