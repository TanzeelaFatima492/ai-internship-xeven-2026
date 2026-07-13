'use client'

import { FileText, DollarSign } from 'lucide-react'

interface MessageProps {
  message: {
    id: string
    role: 'user' | 'ai'
    content: string
    source?: string
    price?: string
    timestamp: Date
  }
}

export default function MessageBubble({ message }: MessageProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-xs md:max-w-md lg:max-w-lg ${
          isUser
            ? 'bg-gradient-to-br from-primary to-accent text-card rounded-2xl rounded-tr-none'
            : 'bg-card border border-border rounded-2xl rounded-tl-none'
        } p-4 md:p-5 shadow-md`}
      >
        <p
          className={`${
            isUser ? 'text-card' : 'text-foreground'
          } text-sm md:text-base leading-relaxed break-words`}
        >
          {message.content}
        </p>

        {/* AI message metadata */}
        {!isUser && (message.source || message.price) && (
          <div className="mt-3 pt-3 border-t border-border/50 space-y-2">
            {message.source && (
              <div className="flex items-center gap-2 text-xs md:text-sm text-muted-foreground">
                <FileText size={16} className="text-primary flex-shrink-0" />
                <span className="font-medium">{message.source}</span>
              </div>
            )}
            {message.price && (
              <div className="flex items-center gap-2 text-xs md:text-sm font-semibold text-primary">
                <DollarSign size={16} className="flex-shrink-0" />
                <span>{message.price}</span>
              </div>
            )}
          </div>
        )}

        {/* Timestamp */}
        <div
          className={`mt-2 text-xs ${
            isUser ? 'text-card/70' : 'text-muted-foreground'
          }`}
        >
          {message.timestamp.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </div>
      </div>
    </div>
  )
}
