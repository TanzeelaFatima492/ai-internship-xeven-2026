import { NextRequest, NextResponse } from 'next/server'
import jwt from 'jsonwebtoken'

// In-memory user storage (in production, use a real database)
let registeredUsers: Record<string, { password: string; email: string }> = {
  admin: {
    password: 'password123',
    email: 'admin@bitwie.com',
  },
}

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production'

export async function POST(request: NextRequest) {
  try {
    const { username, email, password } = await request.json()

    // Validation
    if (!username || !email || !password) {
      return NextResponse.json(
        { error: 'Username, email, and password are required' },
        { status: 400 }
      )
    }

    // Validate username length
    if (username.length < 3) {
      return NextResponse.json(
        { error: 'Username must be at least 3 characters' },
        { status: 400 }
      )
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      return NextResponse.json(
        { error: 'Invalid email format' },
        { status: 400 }
      )
    }

    // Validate password length
    if (password.length < 6) {
      return NextResponse.json(
        { error: 'Password must be at least 6 characters' },
        { status: 400 }
      )
    }

    // Check if username already exists
    if (registeredUsers[username]) {
      return NextResponse.json(
        { error: 'Username already exists' },
        { status: 409 }
      )
    }

    // Check if email already exists
    const emailExists = Object.values(registeredUsers).some(
      (user) => user.email === email
    )
    if (emailExists) {
      return NextResponse.json(
        { error: 'Email already registered' },
        { status: 409 }
      )
    }

    // Create new user
    registeredUsers[username] = {
      password, // In production, hash the password
      email,
    }

    // Create JWT token
    const token = jwt.sign(
      {
        username,
        email,
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
          email,
        },
        message: 'Account created successfully',
      },
      { status: 201 }
    )
  } catch (error) {
    console.error('Signup error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
