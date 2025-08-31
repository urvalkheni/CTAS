# Login Debug Test

Try this sequence to debug the login issue:

## 1. First, register a test user
```http
POST http://localhost:5001/api/auth/register
Content-Type: application/json

{
  "name": "Test User",
  "email": "test@example.com",
  "password": "password123"
}
```

## 2. Then try to login with the same credentials
```http
POST http://localhost:5001/api/auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}
```

## 3. Check server logs for specific error messages

If the login still fails, the issue might be:
1. Password comparison not working properly
2. User not found (case sensitivity)
3. Database connection issue
4. Missing bcrypt comparison

Let me know what error message you get and I'll fix it immediately.
