/* eslint-disable @typescript-eslint/no-explicit-any */
'use client'

import { useState } from 'react'
import { useApi } from '@/hooks/use-api'
import { useApiError } from '@/hooks/use-api-error'
import { ApiError } from '@/lib/api-client'
import ApiErrorNotification from './api-error-notification'
import { Loader2 } from 'lucide-react'

/**
 * Example component demonstrating API client usage with error handling
 * This component shows various API patterns and error handling scenarios
 */
export default function ApiExample() {
  const { get, post, loading, error: apiError } = useApi<any>()
  const { error, handleError, clearError } = useApiError()
  const [responseData, setResponseData] = useState<any>(null)

  // Example 1: GET request
  const handleGetMenu = async () => {
    try {
      const data = await get('/api/menu')
      setResponseData(data)
    } catch (err) {
      handleError(err)
    }
  }

  // Example 2: POST request
  const handlePostChat = async () => {
    try {
      const data = await post('/api/chat', {
        message: 'What are your vegetarian options?',
      })
      setResponseData(data)
    } catch (err) {
      handleError(err)
    }
  }

  // Example 3: Handling rate limiting
  const handleRateLimitTest = async () => {
    try {
      for (let i = 0; i < 10; i++) {
        await post('/api/test', { query: i })
      }
    } catch (err) {
      if (err instanceof ApiError && err.status === 429) {
        console.log('Rate limited - implement backoff strategy')
      }
      handleError(err)
    }
  }

  return (
    <div className="p-6 bg-card border border-border rounded-lg space-y-4">
      <h2 className="text-2xl font-bold text-foreground">API Client Examples</h2>

      {/* Error Notification */}
      <ApiErrorNotification
        message={error.message}
        type={error.type || undefined}
        status={error.status}
        onClose={clearError}
      />

      {/* Examples Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* GET Example */}
        <div className="p-4 bg-background border border-border rounded-lg">
          <h3 className="font-semibold text-foreground mb-3">
            Example 1: GET Request
          </h3>
          <p className="text-sm text-muted-foreground mb-4">
            Fetch menu items from the backend API with automatic JWT token
            attachment
          </p>
          <button
            onClick={handleGetMenu}
            disabled={loading}
            className="w-full px-4 py-2 bg-primary hover:bg-primary/90 disabled:bg-primary/50 text-primary-foreground rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
          >
            {loading && <Loader2 className="w-4 h-4 animate-spin" />}
            Fetch Menu
          </button>
        </div>

        {/* POST Example */}
        <div className="p-4 bg-background border border-border rounded-lg">
          <h3 className="font-semibold text-foreground mb-3">
            Example 2: POST Request
          </h3>
          <p className="text-sm text-muted-foreground mb-4">
            Send a chat message to the AI assistant with error handling
          </p>
          <button
            onClick={handlePostChat}
            disabled={loading}
            className="w-full px-4 py-2 bg-accent hover:bg-accent/90 disabled:bg-accent/50 text-accent-foreground rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
          >
            {loading && <Loader2 className="w-4 h-4 animate-spin" />}
            Send Chat Message
          </button>
        </div>

        {/* Rate Limiting Example */}
        <div className="p-4 bg-background border border-border rounded-lg">
          <h3 className="font-semibold text-foreground mb-3">
            Example 3: Rate Limiting Handling
          </h3>
          <p className="text-sm text-muted-foreground mb-4">
            Demonstrates automatic 429 error handling with user-friendly message
          </p>
          <button
            onClick={handleRateLimitTest}
            disabled={loading}
            className="w-full px-4 py-2 bg-secondary hover:bg-secondary/90 disabled:bg-secondary/50 text-secondary-foreground rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
          >
            {loading && <Loader2 className="w-4 h-4 animate-spin" />}
            Test Rate Limit
          </button>
        </div>

        {/* Authorization Example */}
        <div className="p-4 bg-background border border-border rounded-lg">
          <h3 className="font-semibold text-foreground mb-3">
            Example 4: Auto 401 Handling
          </h3>
          <p className="text-sm text-muted-foreground mb-4">
            Invalid tokens trigger automatic redirect to login page
          </p>
          <button
            disabled={loading}
            className="w-full px-4 py-2 bg-destructive/20 hover:bg-destructive/30 disabled:bg-destructive/10 text-destructive rounded-lg font-medium transition-colors cursor-not-allowed"
          >
            Handled Automatically
          </button>
        </div>
      </div>

      {/* Response Display */}
      {responseData && (
        <div className="p-4 bg-background border border-border rounded-lg">
          <h3 className="font-semibold text-foreground mb-2">Response Data</h3>
          <pre className="text-xs bg-card p-3 rounded border border-border overflow-auto max-h-32 text-muted-foreground">
            {JSON.stringify(responseData, null, 2)}
          </pre>
        </div>
      )}

      {/* Implementation Info */}
      <div className="p-4 bg-primary/5 border border-primary/20 rounded-lg">
        <h3 className="font-semibold text-foreground mb-2">
          Implementation Details
        </h3>
        <ul className="text-sm text-muted-foreground space-y-1 list-disc list-inside">
          <li>JWT token automatically attached to all requests</li>
          <li>401 errors redirect to login page automatically</li>
          <li>429 errors show user-friendly rate limit message</li>
          <li>Network timeouts after 30 seconds by default</li>
          <li>Supports GET, POST, PUT, PATCH, DELETE methods</li>
          <li>Full TypeScript support with proper typing</li>
        </ul>
      </div>

      {/* Configuration Info */}
      <div className="p-4 bg-secondary/5 border border-secondary/20 rounded-lg">
        <h3 className="font-semibold text-foreground mb-2">
          Current Configuration
        </h3>
        <dl className="text-sm text-muted-foreground space-y-1">
          <div>
            <dt className="font-medium text-foreground">API Base URL:</dt>
            <dd>{process.env.NEXT_PUBLIC_API_BASE_URL}</dd>
          </div>
          <div>
            <dt className="font-medium text-foreground">Request Timeout:</dt>
            <dd>
              {process.env.NEXT_PUBLIC_API_TIMEOUT || '30000'}ms
            </dd>
          </div>
          <div>
            <dt className="font-medium text-foreground">Debug Mode:</dt>
            <dd>
              {process.env.NEXT_PUBLIC_API_DEBUG === 'true' ? 'Enabled' : 'Disabled'}
            </dd>
          </div>
        </dl>
      </div>
    </div>
  )
}
