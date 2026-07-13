import { formatDistanceToNow } from 'date-fns'
import { Clock } from 'lucide-react'

interface Query {
  id: string
  question: string
  timestamp: Date
  category: string
}

const queries: Query[] = [
  {
    id: '1',
    question: "What's your cheapest item?",
    timestamp: new Date(Date.now() - 5 * 60000),
    category: 'Menu',
  },
  {
    id: '2',
    question: 'Do you deliver to my area?',
    timestamp: new Date(Date.now() - 15 * 60000),
    category: 'Policies',
  },
  {
    id: '3',
    question: 'Any spicy options?',
    timestamp: new Date(Date.now() - 25 * 60000),
    category: 'Dietary',
  },
  {
    id: '4',
    question: 'Weekend special offers?',
    timestamp: new Date(Date.now() - 45 * 60000),
    category: 'Offers',
  },
  {
    id: '5',
    question: 'Gluten-free menu available?',
    timestamp: new Date(Date.now() - 65 * 60000),
    category: 'Dietary',
  },
]

const categoryColors: Record<string, string> = {
  Menu: 'bg-primary/10 text-primary',
  Dietary: 'bg-accent/10 text-accent',
  Policies: 'bg-secondary/10 text-secondary',
  Offers: 'bg-green-500/10 text-green-500',
}

export default function RecentQueriesList() {
  return (
    <div className="bg-card border border-border rounded-xl p-6">
      <div className="mb-6">
        <h3 className="text-lg font-bold text-foreground mb-2">Recent Queries</h3>
        <p className="text-sm text-muted-foreground">
          Latest user questions from the past hour
        </p>
      </div>

      <div className="space-y-3">
        {queries.map((query) => (
          <div
            key={query.id}
            className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 p-4 rounded-lg bg-background/50 hover:bg-background transition-colors border border-transparent hover:border-border"
          >
            <div className="flex-1">
              <p className="text-foreground font-medium mb-2">{query.question}</p>
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <Clock size={14} />
                <span>{formatDistanceToNow(query.timestamp, { addSuffix: true })}</span>
              </div>
            </div>
            <span
              className={`px-3 py-1 rounded-full text-xs font-semibold whitespace-nowrap ${
                categoryColors[query.category] || 'bg-muted text-muted-foreground'
              }`}
            >
              {query.category}
            </span>
          </div>
        ))}
      </div>

      <button className="w-full mt-6 px-4 py-2 border border-border rounded-lg text-foreground hover:bg-background/50 transition-colors font-medium text-sm">
        View All Queries
      </button>
    </div>
  )
}
