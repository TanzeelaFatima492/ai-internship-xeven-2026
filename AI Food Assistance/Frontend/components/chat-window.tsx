'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Menu, Loader2 } from 'lucide-react'
import MessageBubble from './message-bubble'
import ChatInput from './chat-input'

interface Message {
  id: string
  role: 'user' | 'ai'
  content: string
  source?: string
  price?: string
  timestamp: Date
}

interface ChatWindowProps {
  user: { username: string; email: string }
  activeThreadId: string | null
  onSaveThread: (thread: any) => void
  onToggleSidebar: () => void
}

export default function ChatWindow({
  user,
  activeThreadId,
  onSaveThread,
  onToggleSidebar,
}: ChatWindowProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Load messages for active thread
  useEffect(() => {
    if (activeThreadId) {
      const savedThreads = localStorage.getItem('chatThreads')
      if (savedThreads) {
        try {
          const threads = JSON.parse(savedThreads)
          const thread = threads.find((t: any) => t.id === activeThreadId)
          if (thread && thread.messages) {
            setMessages(thread.messages.map((m: any) => ({
              ...m,
              timestamp: new Date(m.timestamp),
            })))
          }
        } catch (err) {
          console.error('Error loading thread:', err)
        }
      }
    } else {
      setMessages([])
    }
  }, [activeThreadId])

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date(),
    }

    const updatedMessages = [...messages, userMessage]
    setMessages(updatedMessages)
    setInput('')
    setLoading(true)

    try {
      // Call AI chat API
      const token = localStorage.getItem('bitewise_auth_token');
const response = await fetch('http://localhost:8000/rag/query', {
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : ''
  },
  body: JSON.stringify({
    question: text,
    top_k: 3,
    conversation_id: activeThreadId || undefined
  }),
})

      if (!response.ok) {
        throw new Error('Failed to get AI response')
      }

      const data = await response.json()

      const aiMessage: Message = {
  id: (Date.now() + 1).toString(),
  role: 'ai',
  content: data.answer,
  source: data.sources?.[0]?.document_name,
  price: data.sources?.[0]?.text?.match(/Rs\s*[\d,]+/)?.[0],
  timestamp: new Date(),
}

      const finalMessages = [...updatedMessages, aiMessage]
      setMessages(finalMessages)

      // Save thread
      const threadId = activeThreadId || `thread-${Date.now()}`
      onSaveThread({
        id: threadId,
        title: text.substring(0, 50) + (text.length > 50 ? '...' : ''),
        createdAt: new Date(),
        preview: text,
        messages: finalMessages,
      })
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'ai',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      }
      setMessages([...updatedMessages, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex-1 flex flex-col overflow-hidden bg-gradient-to-b from-background to-background/95">
      {/* Chat Header */}
      <div className="border-b border-border bg-card/50 backdrop-blur-sm px-4 md:px-6 py-4 flex items-center justify-between">
        <button
          onClick={onToggleSidebar}
          className="lg:hidden p-2 hover:bg-muted rounded-lg transition-colors"
          aria-label="Toggle sidebar"
        >
          <Menu size={20} className="text-foreground" />
        </button>

        <div>
          <h2 className="text-lg md:text-xl font-semibold text-foreground">
            {activeThreadId ? 'Conversation' : 'New Chat'}
          </h2>
          <p className="text-xs md:text-sm text-muted-foreground">
            Ask about menu items, prices, offers & policies
          </p>
        </div>

        <div className="w-8" /> {/* Spacer for alignment */}
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-primary/10 via-accent/10 to-secondary/10 rounded-full flex items-center justify-center mb-4">
              <ChefHat className="w-8 h-8 text-primary" />
            </div>
            <h3 className="text-lg md:text-xl font-semibold text-foreground mb-2">
              Welcome to BiteWise
            </h3>
            <p className="text-muted-foreground max-w-md text-sm md:text-base">
              Ask me about our authentic Pakistani menu, prices, special offers, or restaurant policies. I&apos;m here to help!
            </p>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            {loading && (
              <div className="flex justify-start mb-4">
                <div className="bg-card border border-border rounded-2xl rounded-tl-none p-4 md:p-5 max-w-xs md:max-w-md">
                  <div className="flex items-center gap-3">
                    <Loader2 className="w-5 h-5 text-primary animate-spin" />
                    <span className="text-muted-foreground">AI is thinking...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t border-border bg-card/50 backdrop-blur-sm px-4 md:px-6 py-4">
        <ChatInput
          value={input}
          onChange={setInput}
          onSend={handleSendMessage}
          disabled={loading}
          placeholder="Ask about menu, prices, or anything else..."
        />
      </div>
    </div>
  )
}

import { ChefHat } from 'lucide-react'
