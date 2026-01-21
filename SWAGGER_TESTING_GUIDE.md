# 🚀 Swagger UI API Testing Guide

## 📍 **Access Swagger UI**

Start your API and visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🔧 **Quick Setup for Testing**

### 1. **Start the API**
```bash
python main.py
```

### 2. **Open Swagger UI**
Navigate to: http://localhost:8000/docs

## 🧪 **Step-by-Step Testing**

### **Step 1: Create Admin (No Auth Required)**
```json
POST /api/v1/admins
{
  "phone": 9876543210,
  "email": "admin@school.com",
  "name": "Test Admin",
  "password": "admin123",
  "dob": "1990-01-01"
}
```

### **Step 2: Admin Login**
```json
POST /api/v1/auth/admin/login
{
  "phone": 9876543210,
  "password": "admin123"
}
```
**Copy the `access_token` from response!**

### **Step 3: Authorize in Swagger**
1. Click **🔒 Authorize** button in Swagger UI
2. Enter: `Bearer YOUR_ACCESS_TOKEN`
3. Click **Authorize**

### **Step 4: Test Protected Endpoints**
Now you can test all admin endpoints:

#### **Create Parent**
```json
POST /api/v1/parents
{
  "phone": 9123456789,
  "name": "Test Parent",
  "parent_role": "MOTHER",
  "city": "Mumbai"
}
```

#### **Create Driver**
```json
POST /api/v1/drivers
{
  "name": "Test Driver",
  "phone": 9987654321,
  "licence_number": "DL123456789"
}
```

#### **Create Route**
```json
POST /api/v1/routes
{
  "name": "Route A"
}
```

#### **Create Bus**
```json
POST /api/v1/buses
{
  "bus_number": "MH01AB1234",
  "seating_capacity": 40,
  "bus_brand": "Tata"
}
```

## 🔐 **Testing OTP Authentication**

### **Step 1: Send OTP to Parent**
```json
POST /api/v1/auth/send-otp
{
  "phone": 9123456789,
  "user_type": "parent"
}
```

### **Step 2: Verify OTP**
```json
POST /api/v1/auth/verify-otp
{
  "phone": 9123456789,
  "otp": "123456",
  "user_type": "parent"
}
```

## 📊 **All Available Endpoints in Swagger**

### 🔐 **Authentication (4 endpoints)**
- `POST /auth/admin/login` - Admin login
- `POST /auth/send-otp` - Send OTP
- `POST /auth/verify-otp` - Verify OTP  
- `POST /auth/resend-otp` - Resend OTP

### 👨💼 **Admins (6 endpoints)**
- `POST /admins` - Create admin
- `GET /admins` - Get all admins
- `GET /admins/me` - Get current admin
- `GET /admins/{id}` - Get admin by ID
- `PUT /admins/{id}` - Update admin
- `DELETE /admins/{id}` - Delete admin

### 👨👩👧👦 **Parents (6 endpoints)**
- `POST /parents` - Create parent
- `GET /parents` - Get all parents
- `GET /parents/me` - Get current parent
- `GET /parents/{id}` - Get parent by ID
- `PUT /parents/{id}` - Update parent
- `DELETE /parents/{id}` - Delete parent

### 🚗 **Drivers (6 endpoints)**
- `POST /drivers` - Create driver
- `GET /drivers` - Get all drivers
- `GET /drivers/available` - Get available drivers
- `GET /drivers/{id}` - Get driver by ID
- `PUT /drivers/{id}` - Update driver
- `DELETE /drivers/{id}` - Delete driver

### 🛣️ **Routes (5 endpoints)**
- `POST /routes` - Create route
- `GET /routes` - Get all routes
- `GET /routes/{id}` - Get route by ID
- `PUT /routes/{id}` - Update route
- `DELETE /routes/{id}` - Delete route

### 🚌 **Buses (5 endpoints)**
- `POST /buses` - Create bus
- `GET /buses` - Get all buses
- `GET /buses/{id}` - Get bus by ID
- `PUT /buses/{id}` - Update bus
- `DELETE /buses/{id}` - Delete bus

### 🚏 **Route Stops (5 endpoints)**
- `POST /route-stops` - Create route stop
- `GET /route-stops` - Get all route stops
- `GET /route-stops/{id}` - Get route stop by ID
- `PUT /route-stops/{id}` - Update route stop
- `DELETE /route-stops/{id}` - Delete route stop

### 🎓 **Students (6 endpoints)**
- `POST /students` - Create student
- `GET /students` - Get all students
- `GET /students/parent/{parent_id}` - Get students by parent
- `GET /students/{id}` - Get student by ID
- `PUT /students/{id}` - Update student
- `DELETE /students/{id}` - Delete student

### 🚌 **Trips (5 endpoints)**
- `POST /trips` - Create trip
- `GET /trips` - Get all trips
- `GET /trips/{id}` - Get trip by ID
- `PUT /trips/{id}` - Update trip
- `DELETE /trips/{id}` - Delete trip

## 🎯 **Swagger UI Features**

### ✅ **What You Can Do:**
- **Try It Out** - Test any endpoint directly
- **View Schemas** - See request/response models
- **Authentication** - Use Bearer token authorization
- **Examples** - Pre-filled request examples
- **Response Codes** - See all possible responses
- **Download OpenAPI** - Export API specification

### 🔧 **Testing Tips:**
1. **Always authorize first** for protected endpoints
2. **Copy UUIDs** from responses to use in other requests
3. **Check response schemas** to understand data structure
4. **Use Try It Out** button for each endpoint
5. **View curl commands** for external testing

## 🚀 **Start Testing Now!**

1. Run: `python main.py`
2. Open: http://localhost:8000/docs
3. Create admin → Login → Authorize → Test all endpoints!

**Your complete API testing environment is ready!** 🎉