# BiteWie AI Food Assistant - Authentication System

## Overview

BiteWie is a modern login/signup authentication system for a Pakistani restaurant AI assistant app. The application features a beautiful dark theme with warm spice colors (orange, brown, cream) and provides a seamless user experience on both mobile and desktop.

## Features

### ✨ UI/UX Features
- **Toggle Tabs**: Smooth switching between Login and Signup modes
- **Dark Theme**: Pakistani restaurant aesthetic with warm food colors
- **Mobile Responsive**: Fully responsive design that works on all devices
- **Error Handling**: Clear, user-friendly error messages for invalid credentials
- **Password Toggle**: Show/hide password visibility
- **Loading States**: Visual feedback during authentication
- **Success Messages**: Confirmation messages after successful signup

### 🔐 Authentication Features
- **Login**: Username + password authentication
- **Signup**: Create new accounts with username, email, and password
- **JWT Tokens**: Secure token-based authentication
- **Input Validation**: Client and server-side validation
- **Session Management**: Automatic redirects based on authentication state
- **LocalStorage**: Token persistence for user sessions

## Getting Started

### Demo Credentials
Use these credentials to test the login:
- **Username**: `admin`
- **Password**: `password123`

### Creating a New Account
1. Click the "Sign Up" tab
2. Enter a username (min 3 characters)
3. Enter a valid email address
4. Create a password (min 6 characters)
5. Click "Sign Up" button
6. You'll be automatically logged in and redirected to the home page

## Project Structure

```
app/
├── page.tsx              # Main auth page with tab switching
├── home/
│   └── page.tsx         # Home page after login
├── api/auth/
│   ├── login/route.ts   # Login endpoint
│   └── signup/route.ts  # Signup endpoint
├── globals.css          # Theme colors and styles
└── layout.tsx           # Root layout with dark theme

components/
├── login-form.tsx       # Login form component
└── signup-form.tsx      # Signup form component
```

## Color Scheme

The app uses warm Pakistani restaurant colors:
- **Primary**: Deep orange (#D84315) - Main brand color
- **Secondary**: Rich brown (#6D4C41) - Accent color
- **Accent**: Warm orange (#FF6F00) - Interactive elements
- **Background**: Dark navy (#1A1A2E) - Main background
- **Card**: Dark slate (#2A2A3E) - Card backgrounds

## API Endpoints

### POST /api/auth/login
Authenticate user with username and password

**Request Body:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Response:**
```json
{
  "token": "jwt_token_here",
  "user": {
    "username": "admin",
    "email": "admin@bitwie.com"
  }
}
```

### POST /api/auth/signup
Create a new user account

**Request Body:**
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "token": "jwt_token_here",
  "user": {
    "username": "newuser",
    "email": "user@example.com"
  },
  "message": "Account created successfully"
}
```

## Error Handling

The app handles various error scenarios:
- **Invalid credentials**: "Invalid username or password"
- **Username exists**: "Username already exists"
- **Email exists**: "Email already registered"
- **Invalid email**: "Please enter a valid email address"
- **Short password**: "Password must be at least 6 characters"
- **Missing fields**: "Username, email, and password are required"

## Form Validation

### Client-Side Validation
- Email format check using regex
- Minimum length requirements
- Required field validation
- Real-time form state

### Server-Side Validation
- Comprehensive input validation
- Username uniqueness check
- Email uniqueness check
- Password length enforcement

## Security Notes

⚠️ **Production Deployment**:
1. Change the `JWT_SECRET` environment variable
2. Hash passwords using bcrypt before storing
3. Use a real database instead of in-memory storage
4. Implement HTTPS
5. Add rate limiting to prevent brute force attacks
6. Store tokens securely (httpOnly cookies recommended)

## Technologies Used

- **Frontend**: React 19, Next.js 16, TypeScript
- **Styling**: Tailwind CSS 4, custom OKLCH color system
- **Authentication**: JWT (jsonwebtoken)
- **Icons**: Lucide React
- **State Management**: React hooks

## Responsive Design

The design is optimized for:
- **Mobile**: 375px - 480px
- **Tablet**: 768px - 1024px
- **Desktop**: 1920px+

All elements scale appropriately and maintain readability across all screen sizes.

## Testing

### Test Login
1. Go to http://localhost:3000
2. Enter username: `admin`
3. Enter password: `password123`
4. Click "Login"
5. You should be redirected to /home

### Test Signup
1. Go to http://localhost:3000
2. Click "Sign Up" tab
3. Fill in the form with new credentials
4. Click "Sign Up"
5. You should be redirected to /home with your new account

### Test Error Handling
1. Go to http://localhost:3000
2. Try login with invalid credentials
3. Error message should appear
4. Try signup with existing username
5. Error message should appear

## Future Enhancements

- Add password reset functionality
- Implement OAuth/social login
- Add email verification
- Multi-factor authentication
- User profile management
- Session timeout handling
- Remember me functionality

## Support

For issues or questions, please refer to the main project documentation.
