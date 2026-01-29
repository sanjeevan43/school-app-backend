# 🚌 School Transport Management API - Complete Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Authentication APIs](#authentication-apis)
3. [Admin APIs](#admin-apis)
4. [Parent APIs](#parent-apis)
5. [Driver APIs](#driver-apis)
6. [Route APIs](#route-apis)
7. [Bus APIs](#bus-apis)
8. [Class APIs](#class-apis)
9. [Route Stop APIs](#route-stop-apis)
10. [Student APIs](#student-apis)
11. [Trip APIs](#trip-apis)
12. [Error Handling APIs](#error-handling-apis)
13. [Stored Procedure APIs](#stored-procedure-apis)
14. [Encryption APIs](#encryption-apis)

---

## 🎯 Overview

**Base URL**: `http://localhost:8080/api/v1`
**Total Endpoints**: 60+
**Authentication**: JWT Bearer Token
**Database**: MySQL

---

## 🔐 Authentication APIs

### 1. Login (Universal)
**Endpoint**: `POST /auth/login`

**Request Body**:
```json
{
  "phone": 9876543210,
  "password": "admin123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Get User Profile
**Endpoint**: `GET /auth/profile`
**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "user_type": "admin",
  "profile": {
    "admin_id": "uuid",
    "phone": 9876543210,
    "name": "Admin Name",
    "email": "admin@school.com"
  }
}
```

---

## 👨💼 Admin APIs

### 3. Create Admin
**Endpoint**: `POST /admins`

**Request Body**:
```json
{
  "phone": 9876543210,
  "email": "admin@school.com",
  "name": "Admin Name",
  "password": "admin123"
}
```

### 4. Get Admin Profile
**Endpoint**: `GET /admins/profile`
**Headers**: `Authorization: Bearer <token>`

### 5. Get All Admins
**Endpoint**: `GET /admins`
**Headers**: `Authorization: Bearer <token>`

### 6. Get Admin by ID
**Endpoint**: `GET /admins/{admin_id}`
**Headers**: `Authorization: Bearer <token>`

### 7. Update Admin
**Endpoint**: `PUT /admins/{admin_id}`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "name": "Updated Name",
  "email": "new@email.com",
  "status": "ACTIVE"
}
```

### 8. Delete Admin
**Endpoint**: `DELETE /admins/{admin_id}`
**Headers**: `Authorization: Bearer <token>`

---

## 👨👩👧👦 Parent APIs

### 9. Create Parent
**Endpoint**: `POST /parents`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "phone": 9123456789,
  "email": "parent@gmail.com",
  "name": "Parent Name",
  "password": "parent123",
  "parent_role": "MOTHER",
  "door_no": "123",
  "street": "MG Road",
  "city": "Mumbai",
  "district": "Mumbai",
  "pincode": "400001",
  "fcm_token": "firebase_token"
}
```

### 10. Get Parent Profile
**Endpoint**: `GET /parents/profile`
**Headers**: `Authorization: Bearer <token>`

### 11. Get All Parents
**Endpoint**: `GET /parents`
**Headers**: `Authorization: Bearer <token>`

### 12. Get Parent by ID
**Endpoint**: `GET /parents/{parent_id}`
**Headers**: `Authorization: Bearer <token>`

### 13. Update Parent
**Endpoint**: `PUT /parents/{parent_id}`
**Headers**: `Authorization: Bearer <token>`

### 14. Delete Parent
**Endpoint**: `DELETE /parents/{parent_id}`
**Headers**: `Authorization: Bearer <token>`

### 15. Update Parent FCM Token
**Endpoint**: `PUT /parents/{parent_id}/fcm-token`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "fcm_token": "new_firebase_token"
}
```

### 16. Assign Student to Parent
**Endpoint**: `PUT /parents/{parent_id}/assign-student`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "student_id": "student_uuid"
}
```

---

## 🚗 Driver APIs

### 17. Create Driver
**Endpoint**: `POST /drivers`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "name": "Driver Name",
  "phone": 9987654321,
  "email": "driver@gmail.com",
  "password": "driver123",
  "dob": "1985-01-15",
  "licence_number": "DL123456789",
  "licence_expiry": "2025-12-31",
  "photo_url": "https://example.com/photo.jpg",
  "fcm_token": "firebase_token"
}
```

### 18. Get All Drivers
**Endpoint**: `GET /drivers`
**Headers**: `Authorization: Bearer <token>`
**Query Parameters**: `driver_id` (optional)

### 19. Get Available Drivers
**Endpoint**: `GET /drivers/available`
**Headers**: `Authorization: Bearer <token>`

### 20. Get Driver by ID
**Endpoint**: `GET /drivers/{driver_id}`
**Headers**: `Authorization: Bearer <token>`

### 21. Update Driver
**Endpoint**: `PUT /drivers/{driver_id}`
**Headers**: `Authorization: Bearer <token>`

### 22. Delete Driver
**Endpoint**: `DELETE /drivers/{driver_id}`
**Headers**: `Authorization: Bearer <token>`

### 23. Update Driver FCM Token
**Endpoint**: `PUT /drivers/{driver_id}/fcm-token`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "fcm_token": "new_firebase_token"
}
```

---

## 🛣️ Route APIs

### 24. Create Route
**Endpoint**: `POST /routes`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "name": "Route A"
}
```

### 25. Get All Routes
**Endpoint**: `GET /routes`
**Headers**: `Authorization: Bearer <token>`

### 26. Get Route by ID
**Endpoint**: `GET /routes/{route_id}`
**Headers**: `Authorization: Bearer <token>`

### 27. Update Route
**Endpoint**: `PUT /routes/{route_id}`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "name": "Updated Route Name",
  "routes_active_status": "ACTIVE"
}
```

### 28. Delete Route
**Endpoint**: `DELETE /routes/{route_id}`
**Headers**: `Authorization: Bearer <token>`

---

## 🚌 Bus APIs

### 29. Create Bus
**Endpoint**: `POST /buses`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "registration_number": "MH01AB1234",
  "driver_id": "driver_uuid",
  "route_id": "route_uuid",
  "vehicle_type": "Mini Bus",
  "bus_brand": "Tata",
  "bus_model": "Starbus",
  "seating_capacity": 30,
  "rc_expiry_date": "2025-12-31",
  "fc_expiry_date": "2024-12-31",
  "rc_book_url": "https://example.com/rc.pdf",
  "fc_certificate_url": "https://example.com/fc.pdf"
}
```

### 30. Get All Buses
**Endpoint**: `GET /buses`
**Headers**: `Authorization: Bearer <token>`

### 31. Get Bus by ID
**Endpoint**: `GET /buses/{bus_id}`
**Headers**: `Authorization: Bearer <token>`

### 32. Update Bus
**Endpoint**: `PUT /buses/{bus_id}`
**Headers**: `Authorization: Bearer <token>`

### 33. Delete Bus
**Endpoint**: `DELETE /buses/{bus_id}`
**Headers**: `Authorization: Bearer <token>`

---

## 🏫 Class APIs

### 34. Create Class
**Endpoint**: `POST /classes`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "class_name": "10th",
  "section": "A",
  "academic_year": "2024-25"
}
```

### 35. Get All Classes
**Endpoint**: `GET /classes`
**Headers**: `Authorization: Bearer <token>`

### 36. Get Class by ID
**Endpoint**: `GET /classes/{class_id}`
**Headers**: `Authorization: Bearer <token>`

### 37. Update Class
**Endpoint**: `PUT /classes/{class_id}`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "class_name": "10th",
  "section": "B",
  "academic_year": "2024-25",
  "status": "ACTIVE"
}
```

### 38. Delete Class
**Endpoint**: `DELETE /classes/{class_id}`
**Headers**: `Authorization: Bearer <token>`

---

## 🚏 Route Stop APIs

### 39. Create Route Stop
**Endpoint**: `POST /route-stops`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "route_id": "route_uuid",
  "stop_name": "Main Gate",
  "latitude": 19.0760,
  "longitude": 72.8777,
  "stop_order": 1
}
```

### 40. Get All Route Stops
**Endpoint**: `GET /route-stops`
**Headers**: `Authorization: Bearer <token>`
**Query Parameters**: `route_id` (optional)

### 41. Get Route Stop by ID
**Endpoint**: `GET /route-stops/{stop_id}`
**Headers**: `Authorization: Bearer <token>`

### 42. Update Route Stop
**Endpoint**: `PUT /route-stops/{stop_id}`
**Headers**: `Authorization: Bearer <token>`

### 43. Delete Route Stop
**Endpoint**: `DELETE /route-stops/{stop_id}`
**Headers**: `Authorization: Bearer <token>`

---

## 👨‍🎓 Student APIs

### 44. Create Student
**Endpoint**: `POST /students`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "parent_id": "parent_uuid",
  "s_parent_id": "secondary_parent_uuid",
  "name": "Student Name",
  "dob": "2010-01-15",
  "class_id": "class_uuid",
  "pickup_route_id": "route_uuid",
  "drop_route_id": "route_uuid",
  "pickup_stop_id": "stop_uuid",
  "pickup_stop_order": 1,
  "drop_stop_id": "stop_uuid",
  "drop_stop_order": 5,
  "emergency_contact": 9876543210,
  "student_photo_url": "https://example.com/photo.jpg"
}
```

### 45. Get All Students
**Endpoint**: `GET /students`
**Headers**: `Authorization: Bearer <token>`

### 46. Get Students by Parent
**Endpoint**: `GET /students/parent/{parent_id}`
**Headers**: `Authorization: Bearer <token>`

### 47. Get Student by ID
**Endpoint**: `GET /students/{student_id}`
**Headers**: `Authorization: Bearer <token>`

### 48. Update Student
**Endpoint**: `PUT /students/{student_id}`
**Headers**: `Authorization: Bearer <token>`

### 49. Delete Student
**Endpoint**: `DELETE /students/{student_id}`
**Headers**: `Authorization: Bearer <token>`

---

## 🚌 Trip APIs

### 50. Create Trip
**Endpoint**: `POST /trips`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "bus_id": "bus_uuid",
  "driver_id": "driver_uuid",
  "route_id": "route_uuid",
  "trip_date": "2024-01-15",
  "trip_type": "MORNING"
}
```

### 51. Get All Trips
**Endpoint**: `GET /trips`
**Headers**: `Authorization: Bearer <token>`
**Query Parameters**: `route_id`, `trip_date` (optional)

### 52. Get Trip by ID
**Endpoint**: `GET /trips/{trip_id}`
**Headers**: `Authorization: Bearer <token>`

### 53. Update Trip
**Endpoint**: `PUT /trips/{trip_id}`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "status": "ONGOING",
  "current_stop_order": 3,
  "started_at": "2024-01-15T07:00:00",
  "ended_at": "2024-01-15T09:00:00"
}
```

### 54. Delete Trip
**Endpoint**: `DELETE /trips/{trip_id}`
**Headers**: `Authorization: Bearer <token>`

---

## ❌ Error Handling APIs

### 55. Create Error Log
**Endpoint**: `POST /error-handling`
**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "error_type": "DATABASE_ERROR",
  "error_code": 500,
  "error_description": "Connection timeout"
}
```

### 56. Get All Error Logs
**Endpoint**: `GET /error-handling`
**Headers**: `Authorization: Bearer <token>`

### 57. Get Error Log by ID
**Endpoint**: `GET /error-handling/{error_id}`
**Headers**: `Authorization: Bearer <token>`

### 58. Update Error Log
**Endpoint**: `PUT /error-handling/{error_id}`
**Headers**: `Authorization: Bearer <token>`

### 59. Delete Error Log
**Endpoint**: `DELETE /error-handling/{error_id}`
**Headers**: `Authorization: Bearer <token>`

---

## 🔄 Stored Procedure APIs

### 60. Get Route Stops (Ordered)
**Endpoint**: `GET /routes/{route_id}/stops`
**Headers**: `Authorization: Bearer <token>`

### 61. Get Pickup Schedule
**Endpoint**: `GET /trips/pickup-schedule`
**Headers**: `Authorization: Bearer <token>`

### 62. Get Drop Schedule
**Endpoint**: `GET /trips/drop-schedule`
**Headers**: `Authorization: Bearer <token>`

### 63. Get Next Stop
**Endpoint**: `GET /trips/{trip_id}/next-stop`
**Headers**: `Authorization: Bearer <token>`

---

## 🔐 Encryption APIs

### 64. Encrypt Text
**Endpoint**: `POST /encrypt`

**Request Body**:
```json
{
  "text": "sensitive data"
}
```

**Response**:
```json
{
  "encrypted_text": "encrypted_string"
}
```

### 65. Decrypt Text
**Endpoint**: `POST /decrypt`

**Request Body**:
```json
{
  "encrypted_text": "encrypted_string"
}
```

**Response**:
```json
{
  "decrypted_text": "sensitive data"
}
```

---

## 📊 Response Format

All responses follow this structure:

**Success Response**:
```json
{
  "id_field": "uuid",
  "field1": "value1",
  "field2": "value2",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Error Response**:
```json
{
  "detail": "Error message"
}
```

## 🔑 Authentication

1. **Login** with phone + password
2. **Use Bearer token** in Authorization header
3. **Token format**: `Authorization: Bearer <access_token>`

## 📝 Status Codes

- `200` - Success
- `201` - Created
- `204` - No Content (Delete)
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

**Total API Endpoints: 65**