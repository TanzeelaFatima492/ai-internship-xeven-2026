import { NextRequest, NextResponse } from 'next/server'
import jwt from 'jsonwebtoken'

// Mock user database
const MOCK_USERS: Record<string, { password: string; email: string }> = {
  admin: {
    password: 'password123',
    email: 'admin@bitwie.com',
  },
  demo: {
    password: 'demo1234',
    email: 'demo@bitwie.com',
  },
}

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production'

export async function POST(request: NextRequest) {
  try {
    const { username, password } = await request.json()

    // Validation
    if (!username || !password) {
      return NextResponse.json(
        { error: 'Username and password are required' },
        { status: 400 }
      )
    }

    // Check if user exists
    const user = MOCK_USERS[username]
    if (!user) {
      return NextResponse.json(
        { error: 'Invalid username or password' },
        { status: 401 }
      )
    }

    // Verify password
    if (user.password !== password) {
      return NextResponse.json(
        { error: 'Invalid username or password' },
        { status: 401 }
      )
    }

    // Create JWT token
    const token = jwt.sign(
      {
        username,
        email: user.email,
        iat: Date.now(),
      },
      JWT_SECRET,
      { expiresIn: '7d' }
    )

    return NextResponse.json(
      {
        token,
        user: {
          username,
          email: user.email,
        },
      },
      { status: 200 }
    )
  } catch (error) {
    console.error('Login error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
