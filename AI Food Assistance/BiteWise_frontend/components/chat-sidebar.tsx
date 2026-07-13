'use client'

import { useState } from 'react'
import { Plus, MessageSquare, X } from 'lucide-react'

interface Thread {
  id: string
  title: string
  createdAt: Date
  preview: string
}

interface ChatSidebarProps {
  threads: Thread[]
  activeThreadId: string | null
  onSelectThread: (threadId: string) => void
  onNewChat: () => void
  sidebarOpen: boolean
  onToggleSidebar: () => void
}

export default function ChatSidebar({
  threads,
  activeThreadId,
  onSelectThread,
  onNewChat,
  sidebarOpen,
  onToggleSidebar,
}: ChatSidebarProps) {
  return (
    <>
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 lg:hidden z-30"
          onClick={onToggleSidebar}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed lg:relative w-64 h-screen bg-card border-r border-border flex flex-col transition-all duration-300 z-40 lg:z-auto ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Header */}
        <div className="p-4 border-b border-border flex items-center justify-between">
          <h3 className="font-semibold text-foreground text-sm">History</h3>
          <button
            onClick={onToggleSidebar}
            className="lg:hidden p-1 hover:bg-muted rounded transition-colors"
            aria-label="Close sidebar"
          >
            <X size={20} />
          </button>
        </div>

        {/* New Chat Button */}
        <button
          onClick={() => {
            onNewChat()
            onToggleSidebar()
          }}
          className="m-4 flex items-center gap-3 w-full px-4 py-3 bg-gradient-to-r from-primary/20 to-accent/20 hover:from-primary/30 hover:to-accent/30 border border-primary/20 rounded-lg transition-all duration-200 text-foreground font-medium text-sm"
        >
          <Plus size={18} />
          New Chat
        </button>

        {/* Threads List */}
        <div className="flex-1 overflow-y-auto px-4 py-2 space-y-2">
          {threads.length === 0 ? (
            <div className="p-4 text-center">
              <MessageSquare
                size={32}
                className="mx-auto mb-2 text-muted-foreground/50"
              />
              <p className="text-xs text-muted-foreground">
                No conversations yet. Start a new chat!
              </p>
            </div>
          ) : (
            threads.map((thread) => (
              <button
                key={thread.id}
                onClick={() => {
                  onSelectThread(thread.id)
                  onToggleSidebar()
                }}
                className={`w-full text-left px-3 py-2 rounded-lg transition-all duration-200 group ${
                  activeThreadId === thread.id
                    ? 'bg-primary/20 border border-primary/30 text-foreground'
                    : 'hover:bg-muted/50 text-muted-foreground hover:text-foreground'
                }`}
              >
                <p className="text-xs md:text-sm font-medium truncate">
                  {thread.title}
                </p>
                <p className="text-xs text-muted-foreground truncate mt-1 group-hover:text-muted-foreground">
                  {new Date(thread.createdAt).toLocaleDateString([], {
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </p>
              </button>
            ))
          )}
        </div>

        {/* Footer Info */}
        <div className="p-4 border-t border-border">
          <p className="text-xs text-muted-foreground text-center">
            Made with for food lovers
          </p>
        </div>
      </div>
    </>
  )
}
