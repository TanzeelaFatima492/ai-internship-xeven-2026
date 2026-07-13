import { useRouter } from 'next/navigation'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
const JWT_STORAGE_KEY = process.env.NEXT_PUBLIC_JWT_STORAGE_KEY || 'bitewise_auth_token'
const API_TIMEOUT = parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || '30000', 10)
const API_DEBUG = process.env.NEXT_PUBLIC_API_DEBUG === 'true'

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: unknown
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export interface ApiRequestOptions extends RequestInit {
  timeout?: number
  skipAuth?: boolean
}

interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

/**
 * Get the stored JWT token from localStorage
 */
export function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem(JWT_STORAGE_KEY)
}

/**
 * Set the JWT token in localStorage
 */
export function setAuthToken(token: string): void {
  if (typeof window === 'undefined') return
  localStorage.setItem(JWT_STORAGE_KEY, token)
}

/**
 * Clear the JWT token from localStorage
 */
export function clearAuthToken(): void {
  if (typeof window === 'undefined') return
  localStorage.removeItem(JWT_STORAGE_KEY)
}

/**
 * Internal function to handle API requests with proper error handling
 */
async function apiRequest<T>(
  endpoint: string,
  options: ApiRequestOptions = {}
): Promise<T> {
  const {
    timeout = API_TIMEOUT,
    skipAuth = false,
    headers = {},
    ...fetchOptions
  } = options

  const url = `${API_BASE_URL}${endpoint}`

  // Build headers
  const requestHeaders: HeadersInit = {
    'Content-Type': 'application/json',
    ...headers,
  }

  // Add JWT token if not skipped
  if (!skipAuth) {
    const token = getAuthToken()
    if (token) {
      requestHeaders['Authorization'] = `Bearer ${token}`
    }
  }

  // Log request in debug mode
  if (API_DEBUG) {
    console.log('[API] Request:', {
      url,
      method: fetchOptions.method || 'GET',
      headers: requestHeaders,
    })
  }

  // Create abort controller for timeout
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), timeout)

  try {
    const response = await fetch(url, {
      ...fetchOptions,
      headers: requestHeaders,
      signal: controller.signal,
    })

    clearTimeout(timeoutId)

    // Handle non-JSON responses
    let data: unknown
    const contentType = response.headers.get('content-type')
    if (contentType?.includes('application/json')) {
      data = await response.json()
    } else {
      data = await response.text()
    }

    if (API_DEBUG) {
      console.log('[API] Response:', {
        status: response.status,
        data,
      })
    }

    // Handle 401 Unauthorized
    if (response.status === 401) {
      clearAuthToken()
      // Redirect to login on client-side only
      if (typeof window !== 'undefined') {
        window.location.href = '/'
      }
      throw new ApiError('Unauthorized. Please login again.', 401, data)
    }

    // Handle 429 Too Many Requests
    if (response.status === 429) {
      throw new ApiError(
        'Too many requests. Please try again later.',
        429,
        data
      )
    }

    // Handle other HTTP errors
    if (!response.ok) {
      const errorMessage =
        (data as ApiResponse<unknown>)?.message ||
        (data as ApiResponse<unknown>)?.error ||
        `HTTP Error ${response.status}`

      throw new ApiError(errorMessage, response.status, data)
    }

    // Return data or the full response
    if (data && typeof data === 'object' && 'data' in data) {
      return (data as ApiResponse<T>).data as T
    }

    return data as T
  } catch (error) {
    clearTimeout(timeoutId)

    if (error instanceof ApiError) {
      throw error
    }

    if (error instanceof TypeError && error.message === 'Failed to fetch') {
      throw new ApiError(
        'Network error. Please check your connection.',
        0,
        error
      )
    }

    if ((error as DOMException).name === 'AbortError') {
      throw new ApiError(
        `Request timeout after ${timeout}ms`,
        408,
        error
      )
    }

    throw new ApiError(
      error instanceof Error ? error.message : 'Unknown error occurred',
      500,
      error
    )
  }
}

/**
 * GET request
 */
export async function apiGet<T>(
  endpoint: string,
  options?: ApiRequestOptions
): Promise<T> {
  return apiRequest<T>(endpoint, {
    ...options,
    method: 'GET',
  })
}

/**
 * POST request
 */
export async function apiPost<T>(
  endpoint: string,
  data?: unknown,
  options?: ApiRequestOptions
): Promise<T> {
  return apiRequest<T>(endpoint, {
    ...options,
    method: 'POST',
    body: data ? JSON.stringify(data) : undefined,
  })
}

/**
 * PUT request
 */
export async function apiPut<T>(
  endpoint: string,
  data?: unknown,
  options?: ApiRequestOptions
): Promise<T> {
  return apiRequest<T>(endpoint, {
    ...options,
    method: 'PUT',
    body: data ? JSON.stringify(data) : undefined,
  })
}

/**
 * PATCH request
 */
export async function apiPatch<T>(
  endpoint: string,
  data?: unknown,
  options?: ApiRequestOptions
): Promise<T> {
  return apiRequest<T>(endpoint, {
    ...options,
    method: 'PATCH',
    body: data ? JSON.stringify(data) : undefined,
  })
}

/**
 * DELETE request
 */
export async function apiDelete<T>(
  endpoint: string,
  options?: ApiRequestOptions
): Promise<T> {
  return apiRequest<T>(endpoint, {
    ...options,
    method: 'DELETE',
  })
}
