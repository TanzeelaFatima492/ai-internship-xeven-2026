import { useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { ApiError } from '@/lib/api-client'

export interface ErrorState {
  message: string | null
  status: number | null
  type: 'error' | 'warning' | 'info' | null
}

/**
 * Hook to handle API errors with user-friendly messages
 */
export function useApiError() {
  const router = useRouter()
  const [error, setError] = useState<ErrorState>({
    message: null,
    status: null,
    type: null,
  })

  const handleError = useCallback((err: unknown) => {
    if (err instanceof ApiError) {
      // Handle 401 Unauthorized
      if (err.status === 401) {
        setError({
          message: 'Your session has expired. Please log in again.',
          status: 401,
          type: 'error',
        })
        // Redirect is already handled in api-client
        return
      }

      // Handle 429 Too Many Requests
      if (err.status === 429) {
        setError({
          message: 'Too many requests. Please wait a moment and try again.',
          status: 429,
          type: 'warning',
        })
        return
      }

      // Handle 404 Not Found
      if (err.status === 404) {
        setError({
          message: 'Resource not found.',
          status: 404,
          type: 'error',
        })
        return
      }

      // Handle 400 Bad Request
      if (err.status === 400) {
        setError({
          message: err.message || 'Invalid request. Please check your input.',
          status: 400,
          type: 'error',
        })
        return
      }

      // Handle 500+ Server Errors
      if (err.status >= 500) {
        setError({
          message: 'Server error. Please try again later.',
          status: err.status,
          type: 'error',
        })
        return
      }

      // Handle network errors
      if (err.status === 0) {
        setError({
          message:
            'Network error. Please check your internet connection.',
          status: 0,
          type: 'error',
        })
        return
      }

      // Generic API error
      setError({
        message: err.message,
        status: err.status,
        type: 'error',
      })
      return
    }

    // Handle unknown errors
    setError({
      message:
        err instanceof Error
          ? err.message
          : 'An unexpected error occurred.',
      status: null,
      type: 'error',
    })
  }, [router])

  const clearError = useCallback(() => {
    setError({
      message: null,
      status: null,
      type: null,
    })
  }, [])

  return {
    error,
    handleError,
    clearError,
    hasError: error.message !== null,
  }
}
