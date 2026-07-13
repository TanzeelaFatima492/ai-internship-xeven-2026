'use client'

import { formatDistanceToNow } from 'date-fns'

interface Question {
  id: string
  question: string
  user: string
  timestamp: Date
  category: string
}

const sampleQuestions: Question[] = [
  {
    id: '1',
    question: "What's the price of butter chicken?",
    user: 'Ahmed Khan',
    timestamp: new Date(Date.now() - 5 * 60000),
    category: 'Menu',
  },
  {
    id: '2',
    question: 'Do you have any vegan options?',
    user: 'Sarah Ali',
    timestamp: new Date(Date.now() - 15 * 60000),
    category: 'Dietary',
  },
  {
    id: '3',
    question: 'What are your delivery hours?',
    user: 'Hassan Shah',
    timestamp: new Date(Date.now() - 32 * 60000),
    category: 'Policies',
  },
  {
    id: '4',
    question: 'Tell me about your biryani varieties',
    user: 'Fatima Hassan',
    timestamp: new Date(Date.now() - 1 * 3600000),
    category: 'Menu',
  },
  {
    id: '5',
    question: 'What are the current offers?',
    user: 'Muhammad Ali',
    timestamp: new Date(Date.now() - 2 * 3600000),
    category: 'Offers',
  },
]

const getCategoryColor = (category: string) => {
  const colors: Record<string, string> = {
    Menu: 'bg-primary/10 text-primary',
    Dietary: 'bg-accent/10 text-accent',
    Policies: 'bg-secondary/10 text-secondary',
    Offers: 'bg-green-500/10 text-green-500',
  }
  return colors[category] || 'bg-muted text-muted-foreground'
}

export default function RecentQuestionsTable() {
  return (
    <div className="bg-card border border-border rounded-xl overflow-hidden">
      <div className="p-6 border-b border-border">
        <h3 className="text-lg font-semibold text-foreground">Recent Questions</h3>
        <p className="text-sm text-muted-foreground">Latest user queries from the past 24 hours</p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-muted/50 border-b border-border">
            <tr>
              <th className="px-6 py-3 text-left font-semibold text-muted-foreground">Question</th>
              <th className="px-6 py-3 text-left font-semibold text-muted-foreground">User</th>
              <th className="px-6 py-3 text-left font-semibold text-muted-foreground">Category</th>
              <th className="px-6 py-3 text-left font-semibold text-muted-foreground">Time</th>
            </tr>
          </thead>
          <tbody>
            {sampleQuestions.map((question) => (
              <tr
                key={question.id}
                className="border-b border-border hover:bg-muted/30 transition-colors"
              >
                <td className="px-6 py-4 text-foreground max-w-xs truncate">
                  {question.question}
                </td>
                <td className="px-6 py-4 text-muted-foreground">{question.user}</td>
                <td className="px-6 py-4">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium ${getCategoryColor(
                      question.category
                    )}`}
                  >
                    {question.category}
                  </span>
                </td>
                <td className="px-6 py-4 text-muted-foreground">
                  {formatDistanceToNow(question.timestamp, { addSuffix: true })}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
