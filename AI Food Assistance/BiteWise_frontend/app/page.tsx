'use client'

import { useState } from 'react'
import { ChefHat } from 'lucide-react'
import LoginForm from '@/components/login-form'
import SignupForm from '@/components/signup-form'

export default function AuthPage() {
  const [activeTab, setActiveTab] = useState<'login' | 'signup'>('login')
  const [loading, setLoading] = useState(false)

  return (
    <main className="min-h-screen bg-gradient-to-b from-background to-background/95 flex items-center justify-center p-4">
      {/* Decorative background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 right-10 w-72 h-72 bg-primary/5 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 left-10 w-72 h-72 bg-secondary/5 rounded-full blur-3xl"></div>
      </div>

      {/* Main container */}
      <div className="relative w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-primary via-accent to-secondary rounded-full blur-lg opacity-75"></div>
              <div className="relative bg-card p-3 rounded-full">
                <ChefHat className="w-8 h-8 text-primary" strokeWidth={1.5} />
              </div>
            </div>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">BiteWie</h1>
          <p className="text-muted-foreground text-sm md:text-base">AI Food Assistant</p>
        </div>

        {/* Auth Card */}
        <div className="bg-card border border-border rounded-2xl shadow-2xl overflow-hidden backdrop-blur-sm">
          {/* Tab Navigation */}
          <div className="flex border-b border-border">
            <button
              onClick={() => setActiveTab('login')}
              className={`flex-1 py-4 px-6 font-semibold transition-all duration-200 text-center relative ${
                activeTab === 'login'
                  ? 'text-primary'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              Login
              {activeTab === 'login' && (
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-primary via-accent to-secondary"></div>
              )}
            </button>
            <button
              onClick={() => setActiveTab('signup')}
              className={`flex-1 py-4 px-6 font-semibold transition-all duration-200 text-center relative ${
                activeTab === 'signup'
                  ? 'text-primary'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              Sign Up
              {activeTab === 'signup' && (
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-primary via-accent to-secondary"></div>
              )}
            </button>
          </div>

          {/* Form Content */}
          <div className="p-6 md:p-8">
            {activeTab === 'login' ? (
              <LoginForm loading={loading} setLoading={setLoading} />
            ) : (
              <SignupForm loading={loading} setLoading={setLoading} />
            )}
          </div>
        </div>

        {/* Footer text */}
        <div className="text-center mt-6">
          <p className="text-xs md:text-sm text-muted-foreground">
            Experience Pakistani cuisine like never before with AI
          </p>
        </div>
      </div>
    </main>
  )
}
