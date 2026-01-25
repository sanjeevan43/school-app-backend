# 🚌 School Transport Management API - Complete Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Authentication APIs](#authentication-apis)
3. [Admin APIs](#admin-apis)
4. [Parent APIs](#parent-apis)
5. [Driver APIs](#driver-apis)
6. [Route APIs](#route-apis)
7. [Bus APIs](#bus-apis)
8. [Route Stop APIs](#route-stop-apis)
9. [Student APIs](#student-apis)
10. [Trip APIs](#trip-apis)
11. [Database Table Models](#database-table-models)

---

## 🎯 Overview

**Purpose**: This API provides a complete backend system for managing school transport operations, including user management, route planning, bus tracking, and trip scheduling.

**Technology Stack**:
- **Framework**: FastAPI (Python)
- **Database**: MySQL (Hostinger)
- **Authentication**: JWT + Password-based login
- **Documentation**: Swagger UI / ReDoc

**Base URL**: `http://localhost:8000/api/v1`

**Total Endpoints**: 50+

---

## 🔐 Authentication APIs

### 1. Login (Universal)
**Endpoint**: `POST /auth/login`

**Why**: Authenticate users (admin, parent, driver) to access protected resources

**What**: Validates phone number and password, returns JWT access token

**When**: Use when any user needs to log into the system

**Authentication Method**: Password-based login for all user types
- Admins: Use password set during account creation
- Parents: Use password set by admin during account creation
- Drivers: Use password set by admin during account creation

**Request Body**:
```json
{
  "phone": 9876543210,
  "password": "admin123"
}
```

**⚠️ Important Validation Rules**:
- `phone`: Must be exactly 10 digits as INTEGER (not string)
- `password`: Required string, minimum 1 character
- Both fields are mandatory

**✅ Correct Format**:
```json
{
  "phone": 9876543210,
  "password": "admin123"
}
```

**❌ Common Errors (422 Validation Error)**:
```json
// Wrong: Phone as string
{
  "phone": "9876543210",
  "password": "admin123"
}

// Wrong: Phone too short/long
{
  "phone": 987654321,
  "password": "admin123"
}

// Wrong: Missing password
{
  "phone": 9876543210
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Sample Data**:
```json
// Admin Login
{
  "phone": 9876543210,
  "password": "admin123"
}

// Parent Login
{
  "phone": 9123456789,
  "password": "parent123"
}

// Driver Login
{
  "phone": 9987654321,
  "password": "driver123"
}
```

---

### 2. Get User Profile
**Endpoint**: `GET /auth/profile`

**Why**: Retrieve the authenticated user's profile information

**What**: Returns user details based on JWT token

**When**: After login, to display user information in the app

**Headers**: 
```
Authorization: Bearer <access_token>
```

**Response**:
```json
{
  "user_type": "admin",
  "profile": {
    "admin_id": "ADM-550e8400-e29b-41d4-a716-446655440000",
    "phone": 9876543210,
    "name": "School Admin",
    "email": "admin@school.com"
  }
}
```

---

## 👨‍💼 Admin APIs

### 3. Create Admin
**Endpoint**: `POST /admins`

**Why**: Set up initial admin account or add new administrators

**What**: Creates a new admin user with password authentication

**When**: First-time setup or when adding new admin staff

**Request Body**:
```json
{
  "phone": 9876543210,
  "email": "admin@school.com",
  "name": "School Admin",
  "password": "admin123",
  "dob": "1985-01-15"
}
```

**Response**:
```json
{
  "admin_id": "ADM-550e8400-e29b-41d4-a716-446655440000",
  "phone": 9876543210,
  "email": "admin@school.com",
  "name": "School Admin",
  "dob": "1985-01-15",
  "status": "ACTIVE",
  "last_login_at": null,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Sample Data**:
```json
{
  "phone": 9876543210,
  "email": "admin@school.com",
  "name": "Rajesh Kumar",
  "password": "SecurePass@123",
  "dob": "1985-05-20"
}
```

---

### 4. Get Admin Profile
**Endpoint**: `GET /admins/profile`

**Why**: Retrieve current admin's profile

**What**: Returns authenticated admin's details

**When**: After admin login, to display profile

**Headers**: `Authorization: Bearer <admin_token>`

**Response**: Same as Create Admin response

---

### 5. Get All Admins
**Endpoint**: `GET /admins`

**Why**: List all administrators in the system

**What**: Returns array of all admin users

**When**: Admin dashboard, user management

**Headers**: `Authorization: Bearer <admin_token>`

**Response**:
```json
[
  {
    "admin_id": "ADM-550e8400-e29b-41d4-a716-446655440000",
    "phone": 9876543210,
    "name": "School Admin",
    "email": "admin@school.com",
    "status": "ACTIVE",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

---

### 6. Get Admin by ID
**Endpoint**: `GET /admins/{admin_id}`

**Why**: Retrieve specific admin details

**What**: Returns single admin's information

**When**: Viewing admin profile, editing admin

**Headers**: `Authorization: Bearer <admin_token>`

**Sample Request**: `GET /admins/ADM-550e8400-e29b-41d4-a716-446655440000`

---

### 7. Update Admin
**Endpoint**: `PUT /admins/{admin_id}`

**Why**: Modify admin information

**What**: Updates admin details (name, email, status, etc.)

**When**: Editing admin profile, changing admin status

**Request Body**:
```json
{
  "name": "Updated Admin Name",
  "email": "newemail@school.com",
  "status": "ACTIVE"
}
```

**Sample Data**:
```json
{
  "name": "Rajesh Kumar Updated",
  "email": "rajesh.new@school.com",
  "dob": "1985-05-20"
}
```

---

### 8. Delete Admin
**Endpoint**: `DELETE /admins/{admin_id}`

**Why**: Remove admin from system

**What**: Deletes admin account

**When**: Removing admin access, cleanup

**Headers**: `Authorization: Bearer <admin_token>`

**Response**:
```json
{
  "message": "Admin deleted successfully"
}
```

---

## 👨‍👩‍👧‍👦 Parent APIs

### 9. Create Parent
**Endpoint**: `POST /parents`

**Why**: Register new parent/guardian in the system

**What**: Creates parent account with contact and address details

**When**: Onboarding new students' parents

**Headers**: `Authorization: Bearer <admin_token>`

**Request Body**:
```json
{
  "phone": 9123456789,
  "email": "parent@gmail.com",
  "name": "Priya Sharma",
  "password": "parent123",
  "dob": "1988-03-20",
  "parent_role": "MOTHER",
  "door_no": "123",
  "street": "MG Road",
  "city": "Mumbai",
  "district": "Mumbai",
  "state": "Maharashtra",
  "country": "India",
  "pincode": "400001",
  "emergency_contact": 9876543210
}
```

**Response**:
```json
{
  "parent_id": "PAR-660e8400-e29b-41d4-a716-446655440000",
  "phone": 9123456789,
  "email": "parent@gmail.com",
  "name": "Priya Sharma",
  "dob": "1988-03-20",
  "parent_role": "MOTHER",
  "door_no": "123",
  "street": "MG Road",
  "city": "Mumbai",
  "district": "Mumbai",
  "state": "Maharashtra",
  "country": "India",
  "pincode": "400001",
  "emergency_contact": 9876543210,
  "status": "ACTIVE",
  "last_login_at": null,
  "failed_login_attempts": 0,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Sample Data**:
```json
// Mother
{
  "phone": 9123456789,
  "email": "priya.sharma@gmail.com",
  "name": "Priya Sharma",
  "password": "SecurePass@123",
  "dob": "1988-03-20",
  "parent_role": "MOTHER",
  "door_no": "45/B",
  "street": "MG Road",
  "city": "Mumbai",
  "district": "Mumbai Suburban",
  "state": "Maharashtra",
  "country": "India",
  "pincode": "400001",
  "emergency_contact": 9876543210
}

// Father
{
  "phone": 9234567890,
  "email": "amit.patel@gmail.com",
  "name": "Amit Patel",
  "password": "SecurePass@123",
  "dob": "1985-07-15",
  "parent_role": "FATHER",
  "door_no": "12/A",
  "street": "Park Street",
  "city": "Pune",
  "district": "Pune",
  "state": "Maharashtra",
  "country": "India",
  "pincode": "411001",
  "emergency_contact": 9123456789
}

// Guardian
{
  "phone": 9345678901,
  "email": "ramesh.uncle@gmail.com",
  "name": "Ramesh Kumar",
  "password": "SecurePass@123",
  "dob": "1975-11-30",
  "parent_role": "GUARDIAN",
  "door_no": "78",
  "street": "Station Road",
  "city": "Nagpur",
  "district": "Nagpur",
  "state": "Maharashtra",
  "country": "India",
  "pincode": "440001",
  "emergency_contact": 9876543210
}
```

---

### 10. Get Parent Profile
**Endpoint**: `GET /parents/profile`

**Why**: Retrieve current parent's profile

**What**: Returns authenticated parent's details

**When**: After parent login, profile display

**Headers**: `Authorization: Bearer <parent_token>`

---

### 11. Get All Parents
**Endpoint**: `GET /parents`

**Why**: List all registered parents

**What**: Returns array of all parents

**When**: Admin viewing parent list, reports

**Headers**: `Authorization: Bearer <admin_token>`

---

### 12. Get Parent by ID
**Endpoint**: `GET /parents/{parent_id}`

**Why**: Retrieve specific parent details

**What**: Returns single parent's information

**When**: Viewing parent profile, student assignment

**Sample Request**: `GET /parents/PAR-660e8400-e29b-41d4-a716-446655440000`

---

### 13. Update Parent
**Endpoint**: `PUT /parents/{parent_id}`

**Why**: Modify parent information

**What**: Updates parent details

**When**: Address change, contact update

**Request Body**:
```json
{
  "email": "newemail@gmail.com",
  "street": "New Street Name",
  "city": "New City",
  "emergency_contact": 9999999999
}
```

**Sample Data**:
```json
{
  "email": "priya.new@gmail.com",
  "street": "New MG Road Extension",
  "city": "Mumbai",
  "pincode": "400002",
  "emergency_contact": 9111111111
}
```

---

### 14. Delete Parent
**Endpoint**: `DELETE /parents/{parent_id}`

**Why**: Remove parent from system

**What**: Deletes parent account

**When**: Student withdrawal, data cleanup

---

## 🚗 Driver APIs

### 15. Create Driver
**Endpoint**: `POST /drivers`

**Why**: Register new bus driver

**What**: Creates driver account with KYC details

**When**: Hiring new driver

**Headers**: `Authorization: Bearer <admin_token>`

**Request Body**:
```json
{
  "name": "Rajesh Kumar",
  "phone": 9987654321,
  "email": "driver@gmail.com",
  "password": "driver123",
  "dob": "1980-07-10",
  "licence_number": "MH01DL123456",
  "licence_expiry": "2025-12-31",
  "aadhar_number": "123456789012",
  "licence_url": "https://example.com/licence.jpg",
  "aadhar_url": "https://example.com/aadhar.jpg",
  "photo_url": "https://example.com/photo.jpg",
  "device_id": "device-12345"
}
```

**Response**:
```json
{
  "driver_id": "DRV-770e8400-e29b-41d4-a716-446655440000",
  "name": "Rajesh Kumar",
  "phone": 9987654321,
  "email": "driver@gmail.com",
  "dob": "1980-07-10",
  "licence_number": "MH01DL123456",
  "licence_expiry": "2025-12-31",
  "aadhar_number": "123456789012",
  "licence_url": "https://example.com/licence.jpg",
  "aadhar_url": "https://example.com/aadhar.jpg",
  "photo_url": "https://example.com/photo.jpg",
  "device_id": "device-12345",
  "kyc_verified": false,
  "is_available": true,
  "status": "ACTIVE",
  "last_active_at": null,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Sample Data**:
```json
// Driver 1
{
  "name": "Rajesh Kumar",
  "phone": 9987654321,
  "email": "rajesh.driver@gmail.com",
  "password": "SecurePass@123",
  "dob": "1980-07-10",
  "licence_number": "MH01DL123456",
  "licence_expiry": "2025-12-31",
  "aadhar_number": "123456789012"
}

// Driver 2
{
  "name": "Suresh Patil",
  "phone": 9876543211,
  "email": "suresh.driver@gmail.com",
  "password": "SecurePass@123",
  "dob": "1975-03-25",
  "licence_number": "MH02DL654321",
  "licence_expiry": "2026-06-30",
  "aadhar_number": "987654321098"
}

// Driver 3
{
  "name": "Mahesh Desai",
  "phone": 9765432109,
  "email": "mahesh.driver@gmail.com",
  "password": "SecurePass@123",
  "dob": "1982-11-15",
  "licence_number": "MH03DL789456",
  "licence_expiry": "2025-09-30",
  "aadhar_number": "456789123456"
}
```

---

### 16. Get All Drivers
**Endpoint**: `GET /drivers`

**Why**: List all drivers

**What**: Returns array of all drivers, optionally filter by driver_id

**When**: Driver management, bus assignment

**Query Parameters**: `?driver_id=DRV-770e8400-e29b-41d4-a716-446655440000` (optional)

---

### 17. Get Available Drivers
**Endpoint**: `GET /drivers/available`

**Why**: Find drivers available for assignment

**What**: Returns only drivers with is_available=true

**When**: Assigning drivers to buses/trips

---

### 18. Get Driver by ID
**Endpoint**: `GET /drivers/{driver_id}`

**Why**: Retrieve specific driver details

**What**: Returns single driver's information

**When**: Viewing driver profile, KYC verification

---

### 19. Update Driver
**Endpoint**: `PUT /drivers/{driver_id}`

**Why**: Modify driver information

**What**: Updates driver details, KYC status, availability

**When**: License renewal, KYC verification, availability change

**Request Body**:
```json
{
  "licence_expiry": "2026-12-31",
  "kyc_verified": true,
  "is_available": false,
  "device_id": "new-device-id"
}
```

**Sample Data**:
```json
{
  "licence_expiry": "2027-12-31",
  "kyc_verified": true,
  "is_available": true,
  "email": "rajesh.updated@gmail.com"
}
```

---

### 20. Delete Driver
**Endpoint**: `DELETE /drivers/{driver_id}`

**Why**: Remove driver from system

**What**: Deletes driver account

**When**: Driver resignation, termination

---

## 🛣️ Route APIs

### 21. Create Route
**Endpoint**: `POST /routes`

**Why**: Define new bus route

**What**: Creates a route with a name

**When**: Setting up new transport routes

**Headers**: `Authorization: Bearer <admin_token>`

**Request Body**:
```json
{
  "name": "Route A - Central Mumbai"
}
```

**Response**:
```json
{
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "name": "Route A - Central Mumbai",
  "status": "ACTIVE",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Sample Data**:
```json
// Route 1
{
  "name": "Route A - Central Mumbai"
}

// Route 2
{
  "name": "Route B - Western Suburbs"
}

// Route 3
{
  "name": "Route C - Eastern Express"
}

// Route 4
{
  "name": "Route D - South Mumbai"
}

// Route 5
{
  "name": "Route E - Navi Mumbai"
}
```

---

### 22. Get All Routes
**Endpoint**: `GET /routes`

**Why**: List all bus routes

**What**: Returns array of all routes

**When**: Route management, student assignment

---

### 23. Get Route by ID
**Endpoint**: `GET /routes/{route_id}`

**Why**: Retrieve specific route details

**What**: Returns single route's information

**When**: Viewing route details, editing route

---

### 24. Update Route
**Endpoint**: `PUT /routes/{route_id}`

**Why**: Modify route information

**What**: Updates route name or status

**When**: Route name change, deactivating route

**Request Body**:
```json
{
  "name": "Route A - Updated Name",
  "status": "INACTIVE"
}
```

**Sample Data**:
```json
{
  "name": "Route A - Central Mumbai (Modified)",
  "status": "ACTIVE"
}
```

---

### 25. Delete Route
**Endpoint**: `DELETE /routes/{route_id}`

**Why**: Remove route from system

**What**: Deletes route

**When**: Route discontinuation

---

## 🚌 Bus APIs

### 26. Create Bus
**Endpoint**: `POST /buses`

**Why**: Register new school bus

**What**: Creates bus with details and documents

**When**: Adding new bus to fleet

**Headers**: `Authorization: Bearer <admin_token>`

**Request Body**:
```json
{
  "bus_number": "MH01AB1234",
  "driver_id": "DRV-770e8400-e29b-41d4-a716-446655440000",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "bus_type": "AC",
  "bus_brand": "Tata",
  "bus_model": "Starbus",
  "seating_capacity": 40,
  "rc_expiry_date": "2025-06-30",
  "fc_expiry_date": "2024-12-31",
  "rc_book_url": "https://example.com/rc.jpg",
  "fc_certificate_url": "https://example.com/fc.jpg",
  "bus_front_url": "https://example.com/front.jpg",
  "bus_back_url": "https://example.com/back.jpg",
  "bus_left_url": "https://example.com/left.jpg",
  "bus_right_url": "https://example.com/right.jpg",
  "assigned_date": "2024-01-15"
}
```

**Response**:
```json
{
  "bus_id": "BUS-990e8400-e29b-41d4-a716-446655440000",
  "bus_number": "MH01AB1234",
  "driver_id": "DRV-770e8400-e29b-41d4-a716-446655440000",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "bus_type": "AC",
  "bus_brand": "Tata",
  "bus_model": "Starbus",
  "seating_capacity": 40,
  "rc_expiry_date": "2025-06-30",
  "fc_expiry_date": "2024-12-31",
  "rc_book_url": "https://example.com/rc.jpg",
  "fc_certificate_url": "https://example.com/fc.jpg",
  "bus_front_url": "https://example.com/front.jpg",
  "bus_back_url": "https://example.com/back.jpg",
  "bus_left_url": "https://example.com/left.jpg",
  "bus_right_url": "https://example.com/right.jpg",
  "assigned_date": "2024-01-15",
  "status": "ACTIVE",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Sample Data**:
```json
// Bus 1 - AC Bus
{
  "bus_number": "MH01AB1234",
  "bus_type": "AC",
  "bus_brand": "Tata",
  "bus_model": "Starbus",
  "seating_capacity": 40,
  "rc_expiry_date": "2025-06-30",
  "fc_expiry_date": "2024-12-31"
}

// Bus 2 - Non-AC Bus
{
  "bus_number": "MH02CD5678",
  "bus_type": "Non-AC",
  "bus_brand": "Ashok Leyland",
  "bus_model": "Lynx",
  "seating_capacity": 35,
  "rc_expiry_date": "2025-08-15",
  "fc_expiry_date": "2025-02-28"
}

// Bus 3 - Mini Bus
{
  "bus_number": "MH03EF9012",
  "bus_type": "Mini",
  "bus_brand": "Force Motors",
  "bus_model": "Traveller",
  "seating_capacity": 20,
  "rc_expiry_date": "2026-01-20",
  "fc_expiry_date": "2025-07-15"
}
```

---

### 27. Get All Buses
**Endpoint**: `GET /buses`

**Why**: List all school buses

**What**: Returns array of all buses

**When**: Fleet management, bus assignment

---

### 28. Get Bus by ID
**Endpoint**: `GET /buses/{bus_id}`

**Why**: Retrieve specific bus details

**What**: Returns single bus's information

**When**: Viewing bus details, maintenance records

---

### 29. Update Bus
**Endpoint**: `PUT /buses/{bus_id}`

**Why**: Modify bus information

**What**: Updates bus details, assignment, documents

**When**: Driver reassignment, route change, document renewal

**Request Body**:
```json
{
  "driver_id": "DRV-new-driver-id",
  "route_id": "RTE-new-route-id",
  "rc_expiry_date": "2026-06-30",
  "status": "ACTIVE"
}
```

**Sample Data**:
```json
{
  "rc_expiry_date": "2026-12-31",
  "fc_expiry_date": "2025-12-31",
  "seating_capacity": 45,
  "status": "ACTIVE"
}
```

---

### 30. Delete Bus
**Endpoint**: `DELETE /buses/{bus_id}`

**Why**: Remove bus from fleet

**What**: Deletes bus record

**When**: Bus decommissioning, sale

---

## 🚏 Route Stop APIs

### 31. Create Route Stop
**Endpoint**: `POST /route-stops`

**Why**: Add bus stop to a route

**What**: Creates stop with location and order

**When**: Defining route stops

**Headers**: `Authorization: Bearer <admin_token>`

**Request Body**:
```json
{
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "stop_name": "Main Gate",
  "latitude": 19.0760,
  "longitude": 72.8777,
  "stop_order": 1
}
```

**Response**:
```json
{
  "stop_id": "STP-aa0e8400-e29b-41d4-a716-446655440000",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "stop_name": "Main Gate",
  "latitude": 19.0760,
  "longitude": 72.8777,
  "stop_order": 1,
  "created_at": "2024-01-15T10:30:00"
}
```

**Sample Data**:
```json
// Stop 1 - School Main Gate
{
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "stop_name": "School Main Gate",
  "latitude": 19.0760,
  "longitude": 72.8777,
  "stop_order": 1
}

// Stop 2 - MG Road Junction
{
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "stop_name": "MG Road Junction",
  "latitude": 19.0800,
  "longitude": 72.8800,
  "stop_order": 2
}

// Stop 3 - Railway Station
{
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "stop_name": "Central Railway Station",
  "latitude": 19.0850,
  "longitude": 72.8850,
  "stop_order": 3
}

// Stop 4 - Market Square
{
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "stop_name": "Market Square",
  "latitude": 19.0900,
  "longitude": 72.8900,
  "stop_order": 4
}

// Stop 5 - Park Avenue
{
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "stop_name": "Park Avenue",
  "latitude": 19.0950,
  "longitude": 72.8950,
  "stop_order": 5
}
```

---

### 32. Get All Route Stops
**Endpoint**: `GET /route-stops`

**Why**: List all stops or stops for a specific route

**What**: Returns array of stops

**When**: Route planning, student assignment

**Query Parameters**: `?route_id=RTE-880e8400-e29b-41d4-a716-446655440000` (optional)

---

### 33. Get Route Stop by ID
**Endpoint**: `GET /route-stops/{stop_id}`

**Why**: Retrieve specific stop details

**What**: Returns single stop's information

**When**: Viewing stop details, editing stop

---

### 34. Update Route Stop
**Endpoint**: `PUT /route-stops/{stop_id}`

**Why**: Modify stop information

**What**: Updates stop name, location, or order

**When**: Stop relocation, name change, reordering

**Request Body**:
```json
{
  "stop_name": "Updated Stop Name",
  "latitude": 19.0765,
  "longitude": 72.8780,
  "stop_order": 2
}
```

**Sample Data**:
```json
{
  "stop_name": "School Main Gate (North)",
  "latitude": 19.0765,
  "longitude": 72.8780,
  "stop_order": 1
}
```

---

### 35. Delete Route Stop
**Endpoint**: `DELETE /route-stops/{stop_id}`

**Why**: Remove stop from route

**What**: Deletes stop

**When**: Route optimization, stop discontinuation

---

## 🎓 Student APIs

### 36. Create Student
**Endpoint**: `POST /students`

**Why**: Register new student for transport

**What**: Creates student with parent and route assignment

**When**: Student enrollment, transport registration

**Headers**: `Authorization: Bearer <admin_token>`

**Request Body**:
```json
{
  "parent_id": "PAR-660e8400-e29b-41d4-a716-446655440000",
  "s_parent_id": "PAR-another-parent-id",
  "name": "Aarav Sharma",
  "dob": "2010-09-15",
  "class_section": "5th A",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "pickup_stop_id": "STP-aa0e8400-e29b-41d4-a716-446655440000",
  "drop_stop_id": "STP-bb0e8400-e29b-41d4-a716-446655440000"
}
```

**Response**:
```json
{
  "student_id": "STU-cc0e8400-e29b-41d4-a716-446655440000",
  "parent_id": "PAR-660e8400-e29b-41d4-a716-446655440000",
  "s_parent_id": "PAR-another-parent-id",
  "name": "Aarav Sharma",
  "dob": "2010-09-15",
  "class_section": "5th A",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "pickup_stop_id": "STP-aa0e8400-e29b-41d4-a716-446655440000",
  "drop_stop_id": "STP-bb0e8400-e29b-41d4-a716-446655440000",
  "student_status": "CURRENT",
  "transport_status": "ACTIVE",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Sample Data**:
```json
// Student 1
{
  "parent_id": "PAR-660e8400-e29b-41d4-a716-446655440000",
  "name": "Aarav Sharma",
  "dob": "2010-09-15",
  "class_section": "5th A",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "pickup_stop_id": "STP-aa0e8400-e29b-41d4-a716-446655440000",
  "drop_stop_id": "STP-bb0e8400-e29b-41d4-a716-446655440000"
}

// Student 2
{
  "parent_id": "PAR-660e8400-e29b-41d4-a716-446655440000",
  "name": "Ananya Sharma",
  "dob": "2012-05-20",
  "class_section": "3rd B",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "pickup_stop_id": "STP-aa0e8400-e29b-41d4-a716-446655440000",
  "drop_stop_id": "STP-bb0e8400-e29b-41d4-a716-446655440000"
}

// Student 3 - Different Parent
{
  "parent_id": "PAR-another-parent-id",
  "name": "Rohan Patel",
  "dob": "2011-03-10",
  "class_section": "4th C",
  "route_id": "RTE-another-route-id",
  "pickup_stop_id": "STP-another-stop-id",
  "drop_stop_id": "STP-another-drop-id"
}
```

---

### 37. Get All Students
**Endpoint**: `GET /students`

**Why**: List all students

**What**: Returns array of all students

**When**: Student management, reports

---

### 38. Get Students by Parent
**Endpoint**: `GET /students/parent/{parent_id}`

**Why**: List students of a specific parent

**What**: Returns array of parent's children

**When**: Parent viewing their children, student assignment

---

### 39. Get Student by ID
**Endpoint**: `GET /students/{student_id}`

**Why**: Retrieve specific student details

**What**: Returns single student's information

**When**: Viewing student profile, editing student

---

### 40. Update Student
**Endpoint**: `PUT /students/{student_id}`

**Why**: Modify student information

**What**: Updates student details, route, stops, status

**When**: Class change, route change, status update

**Request Body**:
```json
{
  "class_section": "6th A",
  "route_id": "RTE-new-route-id",
  "pickup_stop_id": "STP-new-pickup-id",
  "drop_stop_id": "STP-new-drop-id",
  "transport_status": "TEMP_STOP"
}
```

**Sample Data**:
```json
{
  "class_section": "6th A",
  "transport_status": "ACTIVE",
  "student_status": "CURRENT"
}
```

---

### 41. Delete Student
**Endpoint**: `DELETE /students/{student_id}`

**Why**: Remove student from transport

**What**: Deletes student record

**When**: Student withdrawal, transport cancellation

---

## 🚌 Trip APIs

### 42. Create Trip
**Endpoint**: `POST /trips`

**Why**: Schedule a bus trip

**What**: Creates trip with bus, driver, route, and date

**When**: Daily trip scheduling

**Headers**: `Authorization: Bearer <admin_token>`

**Request Body**:
```json
{
  "bus_id": "BUS-990e8400-e29b-41d4-a716-446655440000",
  "driver_id": "DRV-770e8400-e29b-41d4-a716-446655440000",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "trip_date": "2024-01-15",
  "trip_type": "MORNING"
}
```

**Response**:
```json
{
  "trip_id": "TRP-dd0e8400-e29b-41d4-a716-446655440000",
  "bus_id": "BUS-990e8400-e29b-41d4-a716-446655440000",
  "driver_id": "DRV-770e8400-e29b-41d4-a716-446655440000",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "trip_date": "2024-01-15",
  "trip_type": "MORNING",
  "status": "NOT_STARTED",
  "current_stop_order": 0,
  "started_at": null,
  "ended_at": null,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Sample Data**:
```json
// Morning Trip
{
  "bus_id": "BUS-990e8400-e29b-41d4-a716-446655440000",
  "driver_id": "DRV-770e8400-e29b-41d4-a716-446655440000",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "trip_date": "2024-01-15",
  "trip_type": "MORNING"
}

// Evening Trip
{
  "bus_id": "BUS-990e8400-e29b-41d4-a716-446655440000",
  "driver_id": "DRV-770e8400-e29b-41d4-a716-446655440000",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "trip_date": "2024-01-15",
  "trip_type": "EVENING"
}

// Different Route Morning Trip
{
  "bus_id": "BUS-another-bus-id",
  "driver_id": "DRV-another-driver-id",
  "route_id": "RTE-another-route-id",
  "trip_date": "2024-01-15",
  "trip_type": "MORNING"
}
```

---

### 43. Get All Trips
**Endpoint**: `GET /trips`

**Why**: List all trips with optional filters

**What**: Returns array of trips

**When**: Trip management, reports, tracking

**Query Parameters**: 
- `?route_id=RTE-880e8400-e29b-41d4-a716-446655440000` (optional)
- `?trip_date=2024-01-15` (optional)

---

### 44. Get Trip by ID
**Endpoint**: `GET /trips/{trip_id}`

**Why**: Retrieve specific trip details

**What**: Returns single trip's information

**When**: Viewing trip details, tracking trip

---

### 45. Update Trip
**Endpoint**: `PUT /trips/{trip_id}`

**Why**: Modify trip status and progress

**What**: Updates trip status, current stop, timestamps

**When**: Trip start, stop updates, trip completion

**Request Body**:
```json
{
  "status": "ONGOING",
  "current_stop_order": 3,
  "started_at": "2024-01-15T07:00:00"
}
```

**Sample Data**:
```json
// Start Trip
{
  "status": "ONGOING",
  "current_stop_order": 1,
  "started_at": "2024-01-15T07:00:00"
}

// Update Progress
{
  "status": "ONGOING",
  "current_stop_order": 3
}

// Complete Trip
{
  "status": "COMPLETED",
  "current_stop_order": 5,
  "ended_at": "2024-01-15T08:30:00"
}

// Pause Trip
{
  "status": "PAUSED",
  "current_stop_order": 2
}
```

---

### 46. Delete Trip
**Endpoint**: `DELETE /trips/{trip_id}`

**Why**: Remove trip from system

**What**: Deletes trip record

**When**: Trip cancellation, cleanup

---

## 🗄️ Database Table Models

### 1. Admins Table
**Table Name**: `admins`

**Purpose**: Store administrator accounts who manage the system

**Columns**:
```sql
admin_id          VARCHAR(50)   PRIMARY KEY    -- Format: ADM-{UUID}
phone             BIGINT        UNIQUE         -- 10-digit phone number
email             VARCHAR(100)  UNIQUE         -- Email address
name              VARCHAR(100)                 -- Admin name
password_hash     VARCHAR(255)                 -- Bcrypt hashed password
dob               DATE                         -- Date of birth
status            ENUM('ACTIVE', 'INACTIVE')   -- Account status
last_login_at     DATETIME                     -- Last login timestamp
created_at        DATETIME                     -- Record creation time
updated_at        DATETIME                     -- Last update time
```

**Sample Record**:
```json
{
  "admin_id": "ADM-550e8400-e29b-41d4-a716-446655440000",
  "phone": 9876543210,
  "email": "admin@school.com",
  "name": "Rajesh Kumar",
  "password_hash": "$2b$12$...",
  "dob": "1985-05-20",
  "status": "ACTIVE",
  "last_login_at": "2024-01-15T10:30:00",
  "created_at": "2024-01-01T09:00:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

---

### 2. Parents Table
**Table Name**: `parents`

**Purpose**: Store parent/guardian information for students

**Columns**:
```sql
parent_id              VARCHAR(50)   PRIMARY KEY    -- Format: PAR-{UUID}
phone                  BIGINT        UNIQUE         -- 10-digit phone number
email                  VARCHAR(100)                 -- Email address
name                   VARCHAR(100)                 -- Parent name
password_hash          VARCHAR(255)                 -- Bcrypt hashed password
dob                    DATE                         -- Date of birth
parent_role            ENUM('FATHER', 'MOTHER', 'GUARDIAN')
door_no                VARCHAR(50)                  -- House/door number
street                 VARCHAR(100)                 -- Street address
city                   VARCHAR(50)                  -- City
district               VARCHAR(50)                  -- District
state                  VARCHAR(50)                  -- State
country                VARCHAR(50)                  -- Country
pincode                VARCHAR(10)                  -- Postal code
emergency_contact      BIGINT                       -- Emergency phone number
status                 ENUM('ACTIVE', 'INACTIVE')   -- Account status
last_login_at          DATETIME                     -- Last login timestamp
failed_login_attempts  INT           DEFAULT 0      -- Failed login counter
created_at             DATETIME                     -- Record creation time
updated_at             DATETIME                     -- Last update time
```

**Sample Record**:
```json
{
  "parent_id": "PAR-660e8400-e29b-41d4-a716-446655440000",
  "phone": 9123456789,
  "email": "priya.sharma@gmail.com",
  "name": "Priya Sharma",
  "password_hash": "$2b$12$...",
  "dob": "1988-03-20",
  "parent_role": "MOTHER",
  "door_no": "45/B",
  "street": "MG Road",
  "city": "Mumbai",
  "district": "Mumbai Suburban",
  "state": "Maharashtra",
  "country": "India",
  "pincode": "400001",
  "emergency_contact": 9876543210,
  "status": "ACTIVE",
  "last_login_at": "2024-01-15T08:00:00",
  "failed_login_attempts": 0,
  "created_at": "2024-01-01T09:00:00",
  "updated_at": "2024-01-15T08:00:00"
}
```

---

### 3. Drivers Table
**Table Name**: `drivers`

**Purpose**: Store bus driver information and KYC details

**Columns**:
```sql
driver_id         VARCHAR(50)   PRIMARY KEY    -- Format: DRV-{UUID}
name              VARCHAR(100)                 -- Driver name
phone             BIGINT        UNIQUE         -- 10-digit phone number
email             VARCHAR(100)                 -- Email address
password_hash     VARCHAR(255)                 -- Bcrypt hashed password
dob               DATE                         -- Date of birth
kyc_verified      BOOLEAN       DEFAULT FALSE  -- KYC verification status
licence_number    VARCHAR(50)                  -- Driving license number
licence_expiry    DATE                         -- License expiry date
aadhar_number     VARCHAR(20)                  -- Aadhar card number
licence_url       VARCHAR(255)                 -- License document URL
aadhar_url        VARCHAR(255)                 -- Aadhar document URL
photo_url         VARCHAR(255)                 -- Driver photo URL
device_id         VARCHAR(255)                 -- Mobile device ID
is_available      BOOLEAN       DEFAULT TRUE   -- Availability status
status            ENUM('ACTIVE', 'INACTIVE')   -- Account status
last_active_at    DATETIME                     -- Last activity timestamp
created_at        DATETIME                     -- Record creation time
updated_at        DATETIME                     -- Last update time
```

**Sample Record**:
```json
{
  "driver_id": "DRV-770e8400-e29b-41d4-a716-446655440000",
  "name": "Rajesh Kumar",
  "phone": 9987654321,
  "email": "rajesh.driver@gmail.com",
  "password_hash": "$2b$12$...",
  "dob": "1980-07-10",
  "kyc_verified": true,
  "licence_number": "MH01DL123456",
  "licence_expiry": "2025-12-31",
  "aadhar_number": "123456789012",
  "licence_url": "https://example.com/licence.jpg",
  "aadhar_url": "https://example.com/aadhar.jpg",
  "photo_url": "https://example.com/photo.jpg",
  "device_id": "device-12345",
  "is_available": true,
  "status": "ACTIVE",
  "last_active_at": "2024-01-15T07:00:00",
  "created_at": "2024-01-01T09:00:00",
  "updated_at": "2024-01-15T07:00:00"
}
```

---

### 4. Routes Table
**Table Name**: `routes`

**Purpose**: Define bus routes

**Columns**:
```sql
route_id      VARCHAR(50)   PRIMARY KEY    -- Format: RTE-{UUID}
name          VARCHAR(100)                 -- Route name
status        ENUM('ACTIVE', 'INACTIVE')   -- Route status
created_at    DATETIME                     -- Record creation time
updated_at    DATETIME                     -- Last update time
```

**Sample Record**:
```json
{
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "name": "Route A - Central Mumbai",
  "status": "ACTIVE",
  "created_at": "2024-01-01T09:00:00",
  "updated_at": "2024-01-01T09:00:00"
}
```

---

### 5. Buses Table
**Table Name**: `buses`

**Purpose**: Store school bus information and documents

**Columns**:
```sql
bus_id              VARCHAR(50)   PRIMARY KEY    -- Format: BUS-{UUID}
bus_number          VARCHAR(20)   UNIQUE         -- Bus registration number
driver_id           VARCHAR(50)   FOREIGN KEY    -- Reference to drivers
route_id            VARCHAR(50)   FOREIGN KEY    -- Reference to routes
bus_type            VARCHAR(50)                  -- AC/Non-AC/Mini
bus_brand           VARCHAR(100)                 -- Bus manufacturer
bus_model           VARCHAR(100)                 -- Bus model
seating_capacity    INT                          -- Number of seats
rc_expiry_date      DATE                         -- RC expiry date
fc_expiry_date      DATE                         -- Fitness certificate expiry
rc_book_url         VARCHAR(255)                 -- RC document URL
fc_certificate_url  VARCHAR(255)                 -- FC document URL
bus_front_url       VARCHAR(255)                 -- Front photo URL
bus_back_url        VARCHAR(255)                 -- Back photo URL
bus_left_url        VARCHAR(255)                 -- Left side photo URL
bus_right_url       VARCHAR(255)                 -- Right side photo URL
assigned_date       DATE                         -- Driver assignment date
status              ENUM('ACTIVE', 'INACTIVE')   -- Bus status
created_at          DATETIME                     -- Record creation time
updated_at          DATETIME                     -- Last update time
```

**Sample Record**:
```json
{
  "bus_id": "BUS-990e8400-e29b-41d4-a716-446655440000",
  "bus_number": "MH01AB1234",
  "driver_id": "DRV-770e8400-e29b-41d4-a716-446655440000",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "bus_type": "AC",
  "bus_brand": "Tata",
  "bus_model": "Starbus",
  "seating_capacity": 40,
  "rc_expiry_date": "2025-06-30",
  "fc_expiry_date": "2024-12-31",
  "rc_book_url": "https://example.com/rc.jpg",
  "fc_certificate_url": "https://example.com/fc.jpg",
  "bus_front_url": "https://example.com/front.jpg",
  "bus_back_url": "https://example.com/back.jpg",
  "bus_left_url": "https://example.com/left.jpg",
  "bus_right_url": "https://example.com/right.jpg",
  "assigned_date": "2024-01-15",
  "status": "ACTIVE",
  "created_at": "2024-01-01T09:00:00",
  "updated_at": "2024-01-15T09:00:00"
}
```

---

### 6. Route Stops Table
**Table Name**: `route_stops`

**Purpose**: Define stops along each route with GPS coordinates

**Columns**:
```sql
stop_id      VARCHAR(50)   PRIMARY KEY    -- Format: STP-{UUID}
route_id     VARCHAR(50)   FOREIGN KEY    -- Reference to routes
stop_name    VARCHAR(100)                 -- Stop name
latitude     DECIMAL(10,8)                -- GPS latitude
longitude    DECIMAL(11,8)                -- GPS longitude
stop_order   INT                          -- Sequence number
created_at   DATETIME                     -- Record creation time
```

**Sample Record**:
```json
{
  "stop_id": "STP-aa0e8400-e29b-41d4-a716-446655440000",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "stop_name": "School Main Gate",
  "latitude": 19.07600000,
  "longitude": 72.87770000,
  "stop_order": 1,
  "created_at": "2024-01-01T09:00:00"
}
```

---

### 7. Students Table
**Table Name**: `students`

**Purpose**: Store student information and transport assignments

**Columns**:
```sql
student_id        VARCHAR(50)   PRIMARY KEY    -- Format: STU-{UUID}
parent_id         VARCHAR(50)   FOREIGN KEY    -- Primary parent reference
s_parent_id       VARCHAR(50)   FOREIGN KEY    -- Secondary parent reference
name              VARCHAR(100)                 -- Student name
dob               DATE                         -- Date of birth
class_section     VARCHAR(50)                  -- Class and section
route_id          VARCHAR(50)   FOREIGN KEY    -- Assigned route
pickup_stop_id    VARCHAR(50)   FOREIGN KEY    -- Pickup stop
drop_stop_id      VARCHAR(50)   FOREIGN KEY    -- Drop stop
student_status    ENUM('CURRENT', 'ALUMNI', 'DISCONTINUED')
transport_status  ENUM('ACTIVE', 'TEMP_STOP', 'CANCELLED')
created_at        DATETIME                     -- Record creation time
updated_at        DATETIME                     -- Last update time
```

**Sample Record**:
```json
{
  "student_id": "STU-cc0e8400-e29b-41d4-a716-446655440000",
  "parent_id": "PAR-660e8400-e29b-41d4-a716-446655440000",
  "s_parent_id": null,
  "name": "Aarav Sharma",
  "dob": "2010-09-15",
  "class_section": "5th A",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "pickup_stop_id": "STP-aa0e8400-e29b-41d4-a716-446655440000",
  "drop_stop_id": "STP-bb0e8400-e29b-41d4-a716-446655440000",
  "student_status": "CURRENT",
  "transport_status": "ACTIVE",
  "created_at": "2024-01-01T09:00:00",
  "updated_at": "2024-01-01T09:00:00"
}
```

---

### 8. Trips Table
**Table Name**: `trips`

**Purpose**: Track daily bus trips and their progress

**Columns**:
```sql
trip_id            VARCHAR(50)   PRIMARY KEY    -- Format: TRP-{UUID}
bus_id             VARCHAR(50)   FOREIGN KEY    -- Reference to buses
driver_id          VARCHAR(50)   FOREIGN KEY    -- Reference to drivers
route_id           VARCHAR(50)   FOREIGN KEY    -- Reference to routes
trip_date          DATE                         -- Trip date
trip_type          ENUM('MORNING', 'EVENING')   -- Trip type
status             ENUM('NOT_STARTED', 'ONGOING', 'PAUSED', 'COMPLETED')
current_stop_order INT           DEFAULT 0      -- Current stop number
started_at         DATETIME                     -- Trip start time
ended_at           DATETIME                     -- Trip end time
created_at         DATETIME                     -- Record creation time
updated_at         DATETIME                     -- Last update time
```

**Sample Record**:
```json
{
  "trip_id": "TRP-dd0e8400-e29b-41d4-a716-446655440000",
  "bus_id": "BUS-990e8400-e29b-41d4-a716-446655440000",
  "driver_id": "DRV-770e8400-e29b-41d4-a716-446655440000",
  "route_id": "RTE-880e8400-e29b-41d4-a716-446655440000",
  "trip_date": "2024-01-15",
  "trip_type": "MORNING",
  "status": "ONGOING",
  "current_stop_order": 3,
  "started_at": "2024-01-15T07:00:00",
  "ended_at": null,
  "created_at": "2024-01-15T06:30:00",
  "updated_at": "2024-01-15T07:30:00"
}
```

---

## 📊 Entity Relationships

```
Admins (manages) → All Entities

Parents (has) → Students
  └─ Students (assigned to) → Routes
      ├─ Routes (has) → Route Stops
      │   ├─ Pickup Stop
      │   └─ Drop Stop
      └─ Routes (used by) → Buses
          └─ Buses (driven by) → Drivers

Trips (combines):
  ├─ Bus
  ├─ Driver
  └─ Route
```

---

## 🔑 Key Features by Entity

### Admins
- Password-based authentication
- Full system access
- User management capabilities
- Create parent and driver accounts

### Parents
- Password-based login (password set by admin)
- View their children's transport details
- Multiple children support
- Emergency contact information

### Drivers
- Password-based login (password set by admin)
- KYC verification
- Availability tracking
- License and document management

### Routes
- Named route definitions
- Active/Inactive status
- Multiple stops support

### Buses
- Complete vehicle documentation
- Driver and route assignment
- Capacity management
- Document expiry tracking

### Route Stops
- GPS coordinates
- Ordered sequence
- Route association

### Students
- Dual parent support
- Route and stop assignment
- Status tracking (current/alumni/discontinued)
- Transport status (active/temp_stop/cancelled)

### Trips
- Daily trip scheduling
- Real-time status tracking
- Stop progress monitoring
- Morning/Evening differentiation

---

## 🚀 Quick Testing Workflow

### Step 1: Setup
```bash
1. Create Admin
2. Login as Admin
3. Copy access_token
4. Authorize in Swagger UI (click 🔒 button)
```

### Step 2: Create Dependencies
```bash
1. Create Parent → Get parent_id
2. Create Driver → Get driver_id
3. Create Route → Get route_id
4. Create Route Stops → Get stop_id (multiple)
5. Create Bus → Get bus_id
```

### Step 3: Create Students and Trips
```bash
1. Create Student (use parent_id, route_id, stop_ids)
2. Create Trip (use bus_id, driver_id, route_id)
```

### Step 4: Test Operations
```bash
1. GET all entities
2. GET by ID
3. UPDATE entities
4. DELETE entities (in reverse order of dependencies)
```

---

## 📱 Mobile App Integration Points

### Parent App Features
- Login with phone + password
- View children's transport details
- Track bus location (via trips)
- View route and stops
- Emergency contact access

### Driver App Features
- Login with phone + password
- View assigned trips
- Update trip status
- Mark current stop
- View route and students

### Admin Dashboard Features
- Complete CRUD operations
- User management
- Route planning
- Trip scheduling
- Reports and analytics

---

## 🔒 Security Features

1. **JWT Authentication**: Secure token-based auth
2. **Password Hashing**: Bcrypt encryption for all user types
3. **Role-based Access**: Admin-only endpoints
4. **Input Validation**: Pydantic models
5. **SQL Injection Prevention**: Parameterized queries
6. **CORS Configuration**: Controlled access
7. **Failed Login Tracking**: Security monitoring
8. **Password-based Login**: Secure authentication for all users

---

## 📞 Support & Documentation

- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **API Version**: 1.0.0

---

## ✅ API Endpoint Summary

| Entity | Create | Read All | Read One | Update | Delete | Total |
|--------|--------|----------|----------|--------|--------|-------|
| Auth | 1 | - | 1 | - | - | 2 |
| Admins | 1 | 1 | 2 | 1 | 1 | 6 |
| Parents | 1 | 1 | 2 | 1 | 1 | 6 |
| Drivers | 1 | 2 | 1 | 1 | 1 | 6 |
| Routes | 1 | 1 | 1 | 1 | 1 | 5 |
| Buses | 1 | 1 | 1 | 1 | 1 | 5 |
| Route Stops | 1 | 1 | 1 | 1 | 1 | 5 |
| Students | 1 | 2 | 1 | 1 | 1 | 6 |
| Trips | 1 | 1 | 1 | 1 | 1 | 5 |
| **Total** | | | | | | **46** |

---

**🎉 Complete API Documentation - Ready for Development!**

---

## 🔧 Fixed Issues Summary

### ✅ Issues Resolved:
1. **Removed OTP Authentication**: Cleaned up unused OTP service code
2. **Unified Password Authentication**: All users (admin, parent, driver) use password-based login
3. **Removed Unwanted Files**: Deleted migration scripts, test files, and backup files
4. **Updated Documentation**: Corrected authentication references throughout
5. **Cleaned Code**: Removed unused imports and helper functions
6. **Streamlined Architecture**: Simplified authentication flow

### 🗂️ Clean File Structure:
- **Core Files**: main.py, routes.py, models.py, database.py, auth.py, config.py, encryption.py
- **Documentation**: COMPLETE_API_DOCUMENTATION.md, README.md
- **Configuration**: .env, .env.example, requirements.txt
- **Deployment**: git-deploy.sh, redeploy.sh

### 🚀 Ready for Production:
- ✅ Password-based authentication for all users
- ✅ JWT token security
- ✅ Complete CRUD operations (46 endpoints)
- ✅ Clean codebase without unused components
- ✅ Comprehensive documentation
- ✅ Production-ready security features
