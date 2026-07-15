'use client'

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
  threads, activeThreadId, onSelectThread, onNewChat, sidebarOpen, onToggleSidebar,
}: ChatSidebarProps) {
  return (
    <>
      {sidebarOpen && <div className="fixed inset-0 bg-black/50 lg:hidden z-30" onClick={onToggleSidebar} />}

      <div className={`fixed lg:relative w-64 h-screen bg-white border-r border-gray-200 flex flex-col transition-all duration-300 z-40 lg:z-auto ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
      }`}>
        {/* Header */}
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          <h3 className="font-semibold text-gray-900 text-sm">History</h3>
          <button onClick={onToggleSidebar} className="lg:hidden p-1 hover:bg-gray-100 rounded">
            <X size={20} className="text-gray-500" />
          </button>
        </div>

        {/* New Chat */}
        <button onClick={() => { onNewChat(); onToggleSidebar() }}
          className="m-4 flex items-center gap-3 px-4 py-3 bg-orange-50 hover:bg-orange-100 border border-orange-200 rounded-lg text-orange-600 font-medium text-sm transition-all">
          <Plus size={18} /> New Chat
        </button>

        {/* Threads */}
        <div className="flex-1 overflow-y-auto px-4 py-2 space-y-1">
          {threads.length === 0 ? (
            <div className="p-4 text-center">
              <MessageSquare size={32} className="mx-auto mb-2 text-gray-300" />
              <p className="text-xs text-gray-400">No conversations yet. Start a new chat!</p>
            </div>
          ) : (
            threads.map((thread) => (
              <button key={thread.id} onClick={() => { onSelectThread(thread.id); onToggleSidebar() }}
                className={`w-full text-left px-3 py-2 rounded-lg transition-all ${
                  activeThreadId === thread.id
                    ? 'bg-orange-50 border border-orange-200 text-orange-700'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}>
                <p className="text-sm font-medium truncate">{thread.title}</p>
                <p className="text-xs text-gray-400 mt-0.5">
                  {new Date(thread.createdAt).toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                </p>
              </button>
            ))
          )}
        </div>

        <div className="p-4 border-t border-gray-200">
          <p className="text-xs text-gray-400 text-center">🍽️ BiteWise Chat</p>
        </div>
      </div>
    </>
  )
}