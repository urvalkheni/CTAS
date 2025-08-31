# CTAS Authentication API Testing Guide

## Server Status
- **Backend Server**: http://localhost:3003
- **Status**: Running with MongoDB Atlas connection retry logic
- **Environment**: Development

## MongoDB Atlas Issues Fixed
✅ **Connection Retry Logic**: Server continues running even if MongoDB is unavailable  
✅ **Detailed Error Messages**: Clear instructions for IP whitelisting  
✅ **Graceful Degradation**: API endpoints work, database operations fail gracefully  

## Authentication System Features

### 🔐 Security Features
- **JWT Authentication** with 7-day expiration
- **bcrypt Password Hashing** with salt rounds: 12
- **Role-based Permissions** (admin, operator, viewer, community_leader)
- **Input Validation** with express-validator
- **Rate Limiting** on API routes

### 👤 User Roles & Permissions
| Role | Create Alerts | Acknowledge Alerts | Generate Reports | Manage Users | View Dashboard | Access API |
|------|---------------|-------------------|------------------|--------------|----------------|------------|
| **admin** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **operator** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **community_leader** | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ |
| **viewer** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

## ThunderClient Testing

### 1. Import Collection
Import the file: `CTAS_Authentication_API.json` into ThunderClient

### 2. Test Sequence

#### Step 1: Health Check
```
GET http://localhost:3003/health
```

#### Step 2: Register Users
```
POST http://localhost:3003/api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@example.com", 
  "password": "Password123",
  "role": "viewer",
  "organization": "Coastal Research Institute",
  "department": "Marine Biology",
  "phone": "+1234567890",
  "region": "East Coast"
}
```

#### Step 3: Login
```
POST http://localhost:3003/api/auth/login
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "Password123"
}
```

**Copy the `token` from login response for next steps**

#### Step 4: Get Profile (Authenticated)
```
GET http://localhost:3003/api/auth/profile
Authorization: Bearer YOUR_TOKEN_HERE
```

#### Step 5: Update Profile (Authenticated)
```
PUT http://localhost:3003/api/auth/profile
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "name": "John Updated",
  "organization": "Updated Organization",
  "preferences": {
    "emailNotifications": false,
    "smsNotifications": true
  }
}
```

#### Step 6: Test Authentication
```
GET http://localhost:3003/api/auth/test
Authorization: Bearer YOUR_TOKEN_HERE
```

## Validation Testing

### ❌ Invalid Email Format
```json
{
  "name": "Test User",
  "email": "invalid-email",
  "password": "Password123"
}
```

### ❌ Weak Password
```json
{
  "name": "Test User", 
  "email": "test@example.com",
  "password": "weak"
}
```

### ❌ Invalid Login
```json
{
  "email": "nonexistent@example.com",
  "password": "WrongPassword123"
}
```

## Response Examples

### ✅ Successful Registration
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "66d1234567890abcdef",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "role": "viewer",
      "status": "active",
      "permissions": {
        "canCreateAlerts": false,
        "canAcknowledgeAlerts": false,
        "canGenerateReports": false,
        "canManageUsers": false,
        "canViewDashboard": true,
        "canAccessAPI": false
      },
      "profile": {
        "organization": "Coastal Research Institute",
        "department": "Marine Biology",
        "phone": "+1234567890",
        "location": {
          "region": "East Coast"
        }
      }
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### ✅ Successful Login
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "user": {
      "id": "66d1234567890abcdef",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "role": "viewer",
      "status": "active",
      "permissions": {...},
      "lastLogin": "2025-08-30T15:10:00.000Z",
      "loginCount": 1
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### ❌ Validation Error
```json
{
  "status": "error",
  "message": "Validation failed",
  "errors": [
    {
      "msg": "Password must contain at least one lowercase letter, one uppercase letter, and one number",
      "param": "password",
      "location": "body"
    }
  ]
}
```

### ❌ Authentication Error
```json
{
  "status": "error",
  "message": "Access token is required"
}
```

## MongoDB Atlas Setup (If needed)

If you get MongoDB connection errors:

1. **Go to MongoDB Atlas Dashboard**
2. **Network Access** → **Add IP Address**
3. **Add** `0.0.0.0/0` (allow all IPs for testing)
4. **Confirm** and wait 2-3 minutes

The server will automatically retry connection every 5 seconds.

## Next Steps

1. **Test all endpoints** in ThunderClient
2. **Verify role-based permissions** by creating admin/operator users
3. **Test token expiration** (tokens expire in 7 days)
4. **Test password changes** and profile updates
5. **Verify validation** with invalid inputs

---

**Server Ready for Testing!** 🚀
