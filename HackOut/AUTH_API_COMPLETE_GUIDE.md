# Complete Authentication API Testing Guide

## 🚀 Quick Start

Your authentication system is now complete with three main endpoints:

### Available Endpoints:
- ✅ **POST** `/api/auth/register` - Register new users with JWT token
- ✅ **POST** `/api/auth/login` - Login users and get JWT token  
- ✅ **POST** `/api/auth/logout` - Logout users (client-side token removal)

## 📋 Test Sequence

### 1. Import ThunderClient Collection
Import: `Complete_Auth_Tests.json`

### 2. Step-by-Step Testing

#### Step 1: Health Check
```http
GET http://localhost:6000/health
```
**Expected:** `Status: 200 OK` with server info

#### Step 2: Register User
```http
POST http://localhost:6000/api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "password123",
  "role": "viewer",
  "organization": "Coastal Research Institute",
  "department": "Marine Biology",
  "phone": "+1234567890",
  "region": "East Coast"
}
```
**Expected:** `201 Created` with user data and JWT token

#### Step 3: Login User
```http
POST http://localhost:6000/api/auth/login
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "password123"
}
```
**Expected:** `200 OK` with user data and JWT token

#### Step 4: Logout User
```http
POST http://localhost:6000/api/auth/logout
```
**Expected:** `200 OK` with logout confirmation

## 🔐 Authentication Features

### Security Implemented:
- ✅ **Password hashing** with bcrypt (automatic in User model)
- ✅ **JWT tokens** with 7-day expiration
- ✅ **Email validation** with regex pattern
- ✅ **Password strength** minimum 6 characters
- ✅ **Duplicate email prevention**
- ✅ **User status checking** (active/inactive/suspended)
- ✅ **Role-based permissions** (admin, operator, viewer, community_leader)

### Response Format:
All responses follow consistent format:
```json
{
  "success": true/false,
  "message": "Description",
  "data": {
    "user": {...},
    "token": "jwt_token_here"
  }
}
```

## 🧪 Validation Tests

### ❌ Should Fail Tests:

1. **Duplicate Email Registration**
   ```json
   {
     "name": "Another User",
     "email": "john.doe@example.com",  // Already exists
     "password": "password123"
   }
   ```

2. **Invalid Login Credentials**
   ```json
   {
     "email": "john.doe@example.com",
     "password": "wrongpassword"
   }
   ```

3. **Non-existent User Login**
   ```json
   {
     "email": "nonexistent@example.com",
     "password": "password123"
   }
   ```

4. **Missing Required Fields**
   ```json
   {
     "email": "john.doe@example.com"
     // Missing password
   }
   ```

## 📊 User Roles & Permissions

| Role | Create Alerts | Acknowledge | Reports | Manage Users | Dashboard | API Access |
|------|---------------|-------------|---------|--------------|-----------|-------------|
| **admin** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **operator** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **community_leader** | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ |
| **viewer** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

## 🎯 Success Response Examples

### Registration Success:
```json
{
  "success": true,
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
      },
      "createdAt": "2025-08-30T15:20:00.000Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### Login Success:
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "66d1234567890abcdef",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "role": "viewer",
      "status": "active",
      "permissions": {...},
      "profile": {...},
      "lastLogin": "2025-08-30T15:21:00.000Z",
      "loginCount": 2
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### Logout Success:
```json
{
  "success": true,
  "message": "Logout successful"
}
```

## ⚠️ Error Response Examples

### Duplicate Email:
```json
{
  "success": false,
  "message": "User with this email already exists"
}
```

### Invalid Login:
```json
{
  "success": false,
  "message": "Invalid email or password"
}
```

### Missing Fields:
```json
{
  "success": false,
  "message": "Email and password are required"
}
```

---

## 🎉 Your Authentication System is Ready!

✅ **Register** - Create new users with profile data  
✅ **Login** - Authenticate and get JWT tokens  
✅ **Logout** - Clean logout process  
✅ **Validation** - Comprehensive input validation  
✅ **Security** - Password hashing, JWT tokens, role permissions  

Start testing with ThunderClient! 🚀
