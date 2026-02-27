# 🔐 Authentication System

## Features Added

✅ **Signup** - Create new account
✅ **Login** - Authenticate user
✅ **Logout** - End session
✅ **Protected Routes** - Require authentication
✅ **Session Management** - 7-day token expiry
✅ **Password Hashing** - PBKDF2 with salt

---

## How It Works

### 1. Sign Up
- Navigate to login page
- Click "Sign Up" tab
- Enter username, email, password
- Account created locally

### 2. Login
- Enter username and password
- Receives authentication token
- Token stored in localStorage
- Valid for 7 days

### 3. Logout
- Click "Logout" button in sidebar
- Token invalidated
- Redirected to login page

---

## Security

🔒 **Password Storage:**
- Hashed with PBKDF2-HMAC-SHA256
- 100,000 iterations
- Unique salt per user
- Never stored in plain text

🔒 **Session Tokens:**
- Cryptographically secure random tokens
- 32-byte URL-safe strings
- Stored locally in `data/sessions.json`
- Auto-expire after 7 days

🔒 **Local Only:**
- All data stored locally
- No cloud authentication
- No external API calls
- Complete privacy

---

## API Endpoints

### POST /auth/signup
```json
{
  "username": "john",
  "password": "secret123",
  "email": "john@example.com"
}
```

### POST /auth/login
```json
{
  "username": "john",
  "password": "secret123"
}
```

### POST /auth/logout
Headers: `Authorization: Bearer <token>`

### GET /auth/verify
Headers: `Authorization: Bearer <token>`

---

## Protected Endpoints

All existing endpoints now require authentication:
- `/upload` - File upload
- `/tasks` - Task management
- `/search` - Document search
- `/confirmations` - Task confirmations

---

## Files Created

✅ `src/auth/auth_manager.py` - Authentication logic
✅ `desktop/src/pages/Login/Login.tsx` - Login/Signup UI
✅ Updated `src/api.py` - Auth endpoints
✅ Updated `desktop/src/app/App.tsx` - Protected routes
✅ Updated `desktop/src/components/Sidebar/Sidebar.tsx` - Logout button

---

## Data Storage

**Users:** `data/users.json`
```json
{
  "john": {
    "email": "john@example.com",
    "password": "hashed_password",
    "salt": "random_salt",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

**Sessions:** `data/sessions.json`
```json
{
  "token_abc123": {
    "username": "john",
    "created_at": "2024-01-01T00:00:00",
    "expires_at": "2024-01-08T00:00:00"
  }
}
```

---

## Status: ✅ COMPLETE

Authentication system fully integrated with zero errors!
