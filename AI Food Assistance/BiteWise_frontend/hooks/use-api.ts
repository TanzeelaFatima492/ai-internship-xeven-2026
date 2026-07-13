import { useCallback, useState } from 'react'
import { ApiError, apiGet, apiPost, apiPut, apiPatch, apiDelete, ApiRequestOptions } from '@/lib/api-client'
import { useApiError } from './use-api-error'

export interface UseApiState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

/**
 * Hook for making API calls with loading and error states
 */
export function useApi<T = unknown>() {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: false,
    error: null,
  })
  const { handleError } = useApiError()

  const execute = useCallback(
    async (
      request: () => Promise<T>,
      onSuccess?: (data: T) => void,
      onError?: (error: ApiError) => void
    ) => {
      setState({ data: null, loading: true, error: null })

      try {
        const result = await request()
        setState({ data: result, loading: false, error: null })
        onSuccess?.(result)
        return result
      } catch (err) {
        const apiError = err instanceof ApiError ? err : new ApiError(
          err instanceof Error ? err.message : 'Unknown error',
          500,
          err
        )
        setState({
          data: null,
          loading: false,
          error: apiError.message,
        })
        handleError(apiError)
        onError?.(apiError)
        throw apiError
      }
    },
    [handleError]
  )

  const get = useCallback(
    (endpoint: string, options?: ApiRequestOptions) =>
      execute(() => apiGet<T>(endpoint, options)),
    [execute]
  )

  const post = useCallback(
    (endpoint: string, data?: unknown, options?: ApiRequestOptions) =>
      execute(() => apiPost<T>(endpoint, data, options)),
    [execute]
  )

  const put = useCallback(
    (endpoint: string, data?: unknown, options?: ApiRequestOptions) =>
      execute(() => apiPut<T>(endpoint, data, options)),
    [execute]
  )

  const patch = useCallback(
    (endpoint: string, data?: unknown, options?: ApiRequestOptions) =>
      execute(() => apiPatch<T>(endpoint, data, options)),
    [execute]
  )

  const remove = useCallback(
    (endpoint: string, options?: ApiRequestOptions) =>
      execute(() => apiDelete<T>(endpoint, options)),
    [execute]
  )

  return {
    state,
    execute,
    get,
    post,
    put,
    patch,
    delete: remove,
    loading: state.loading,
    error: state.error,
    data: state.data,
  }
}
