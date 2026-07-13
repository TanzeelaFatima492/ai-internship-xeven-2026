'use client'

import { useState } from 'react'
import { ChefHat } from 'lucide-react'
import LoginForm from '@/components/login-form'
import SignupForm from '@/components/signup-form'

export default function AuthPage() {
  const [activeTab, setActiveTab] = useState<'login' | 'signup'>('login')

  return (
    <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-orange-50 flex items-center justify-center p-4">
      {/* Decorative elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 right-10 w-72 h-72 bg-orange-200 rounded-full blur-3xl opacity-30"></div>
        <div className="absolute bottom-20 left-10 w-72 h-72 bg-orange-100 rounded-full blur-3xl opacity-30"></div>
      </div>

      <div className="relative w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="bg-gradient-to-br from-orange-500 to-orange-600 p-4 rounded-2xl shadow-lg">
              <ChefHat className="w-10 h-10 text-white" />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-1">BiteWise</h1>
          <p className="text-gray-500">AI Food Assistant</p>
        </div>

        {/* Auth Card */}
        <div className="bg-white border border-gray-200 rounded-2xl shadow-xl overflow-hidden">
          {/* Tabs */}
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab('login')}
              className={`flex-1 py-4 font-semibold transition-all text-center relative ${
                activeTab === 'login' ? 'text-orange-500' : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              Login
              {activeTab === 'login' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-orange-500"></div>}
            </button>
            <button
              onClick={() => setActiveTab('signup')}
              className={`flex-1 py-4 font-semibold transition-all text-center relative ${
                activeTab === 'signup' ? 'text-orange-500' : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              Sign Up
              {activeTab === 'signup' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-orange-500"></div>}
            </button>
          </div>

          {/* Form */}
          <div className="p-6 md:p-8">
            {activeTab === 'login' ? <LoginForm /> : <SignupForm />}
          </div>
        </div>

        <p className="text-center text-gray-400 text-sm mt-6">
          Experience Pakistani cuisine like never before with AI
        </p>
      </div>
    </main>
  )
}