# School Transport Management API Documentation

## Base Information

- **Base URL**: `http://72.61.250.191:8080/api/v1`
- **API Version**: 1.0.0
- **Authentication**: JWT Bearer Token

---

## Authentication

All endpoints (except login and admin creation) require a JWT token in the Authorization header:
```
Authorization: Bearer <your_token_here>
```

### 1. Login
**Endpoint**: `POST /auth/login`

**Description**: Universal login for admins, parents, and drivers

**Request Body**:
```json
{
  "phone": 9876543210,
  "password": "your_password"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Get Profile
**Endpoint**: `GET /auth/profile?phone={phone_number}`

**Description**: Get user profile by phone number

**Response**:
```json
{
  "user_type": "admin",
  "user_id": "uuid",
  "phone": 9876543210,
  "email": "admin@school.com",
  "name": "Admin Name",
  "status": "ACTIVE",
  "created_at": "2024-01-01T00:00:00"
}
```

---

## Admins

### 1. Create Admin
**Endpoint**: `POST /admins`

**Request Body**:
```json
{
  "phone": 9876543210,
  "email": "admin@school.com",
  "name": "Admin Name",
  "password": "securepass"
}
```

### 2. Get All Admins
**Endpoint**: `GET /admins`

**Response**: Array of admin objects

### 3. Get Admin by ID
**Endpoint**: `GET /admins/{admin_id}`

### 4. Update Admin
**Endpoint**: `PUT /admins/{admin_id}`

**Request Body** (all fields optional):
```json
{
  "phone": 9876543210,
  "email": "newemail@school.com",
  "name": "New Name",
  "status": "ACTIVE"
}
```

### 5. Update Admin Status
**Endpoint**: `PUT /admins/{admin_id}/status`

**Request Body**:
```json
{
  "status": "INACTIVE"
}
```

### 6. Delete Admin
**Endpoint**: `DELETE /admins/{admin_id}`

---

## Parents

### 1. Create Parent
**Endpoint**: `POST /parents`

**Request Body**:
```json
{
  "phone": 9876543210,
  "email": "parent@example.com",
  "name": "Parent Name",
  "password": "securepass",
  "parent_role": "FATHER",
  "door_no": "123",
  "street": "Main Street",
  "city": "Chennai",
  "district": "Chennai",
  "pincode": "600001"
}
```

**Parent Role Options**: `FATHER`, `MOTHER`, `GUARDIAN`

### 2. Get All Parents
**Endpoint**: `GET /parents`

### 3. Get Parent by ID
**Endpoint**: `GET /parents/{parent_id}`

### 4. Update Parent
**Endpoint**: `PUT /parents/{parent_id}`

### 5. Update Parent Status
**Endpoint**: `PUT /parents/{parent_id}/status`

**Request Body**:
```json
{
  "status": "ACTIVE"
}
```

### 6. Update Parent FCM Token (PUT)
**Endpoint**: `PUT /parents/{parent_id}/fcm-token`

**Request Body**:
```json
{
  "fcm_token": "firebase_token_here"
}
```

### 7. Update Parent FCM Token (PATCH)
**Endpoint**: `PATCH /parents/{parent_id}/fcm-token`

**Request Body**:
```json
{
  "fcm_token": "firebase_token_here"
}
```

### 8. Get All Parent FCM Tokens
**Endpoint**: `GET /parents/fcm-tokens/all`

**Response**:
```json
{
  "parents": [
    {
      "parent_id": "uuid",
      "name": "Parent Name",
      "phone": 9876543210,
      "fcm_token": "token",
      "parents_active_status": "ACTIVE"
    }
  ],
  "count": 1
}
```

### 9. Delete Parent
**Endpoint**: `DELETE /parents/{parent_id}`

---

## Drivers

### 1. Create Driver
**Endpoint**: `POST /drivers`

**Request Body**:
```json
{
  "name": "Driver Name",
  "phone": 9876543210,
  "email": "driver@example.com",
  "licence_number": "DL1234567890",
  "licence_expiry": "2025-12-31",
  "password": "securepass",
  "fcm_token": "firebase_token"
}
```

### 2. Get All Drivers
**Endpoint**: `GET /drivers`

### 3. Get Driver by ID
**Endpoint**: `GET /drivers/{driver_id}`

### 4. Update Driver
**Endpoint**: `PUT /drivers/{driver_id}`

### 5. Update Driver Status
**Endpoint**: `PUT /drivers/{driver_id}/status`

**Request Body**:
```json
{
  "status": "ACTIVE"
}
```

**Available Status Values**: `ACTIVE`, `INACTIVE`, `SUSPENDED`

### 6. Update Driver FCM Token (PATCH)
**Endpoint**: `PATCH /drivers/{driver_id}/fcm-token`

**Request Body**:
```json
{
  "fcm_token": "firebase_token_here"
}
```

### 7. Get All Driver FCM Tokens
**Endpoint**: `GET /drivers/fcm-tokens/all`

**Response**:
```json
{
  "drivers": [
    {
      "driver_id": "uuid",
      "name": "Driver Name",
      "phone": 9876543210,
      "fcm_token": "token",
      "status": "ACTIVE"
    }
  ],
  "count": 1
}
```

### 8. Delete Driver
**Endpoint**: `DELETE /drivers/{driver_id}`

---

## Students

### 1. Create Student
**Endpoint**: `POST /students`

**Description**: Create a new student. Provides specific error messages for invalid references (Parent, Route, Stop, etc.).

**Request Body**:
```json
{
  "parent_id": "parent_uuid",
  "s_parent_id": "secondary_parent_uuid",
  "name": "Student Name",
  "dob": "2015-05-15",
  "class_id": "class_uuid",
  "pickup_route_id": "route_uuid",
  "drop_route_id": "route_uuid",
  "pickup_stop_id": "stop_uuid",
  "drop_stop_id": "stop_uuid",
  "emergency_contact": 9876543210,
  "student_photo_url": "https://example.com/photo.jpg"
}
```

### 2. Get All Students
**Endpoint**: `GET /students`

### 3. Get Student by ID
**Endpoint**: `GET /students/{student_id}`

### 4. Update Student
**Endpoint**: `PUT /students/{student_id}`

### 5. Update Student Transport Status
**Endpoint**: `PUT /students/{student_id}/status`

**Request Body**:
```json
{
  "status": "ACTIVE"
}
```

**Transport Status Options**: `ACTIVE`, `TEMP_STOP`, `CANCELLED`

### 6. Assign/Unassign Secondary Parent (PATCH)
**Endpoint**: `PATCH /students/{student_id}/secondary-parent`

**Description**: Assign a secondary parent to a student. Pass `null` to unassign.

**Request Body**:
```json
{
  "s_parent_id": "secondary_parent_uuid"
}
```

### 7. Reassign Primary Parent (PATCH)
**Endpoint**: `PATCH /students/{student_id}/primary-parent`

**Description**: Reassign the primary parent for a student.

**Request Body**:
```json
{
  "parent_id": "primary_parent_uuid"
}
```

### 8. Switch Primary and Secondary Parents (POST)
**Endpoint**: `POST /students/{student_id}/switch-parents`

**Description**: Swap the roles of primary and secondary parents for a student. Requires the student to already have a secondary parent assigned.

**Response**: Updated student object.

### 9. Upgrade Student Class (PATCH)
**Endpoint**: `PATCH /students/{student_id}/upgrade`

**Description**: Promote a student to a new class and optionally update their study year.

**Request Body**:
```json
{
  "new_class_id": "new_class_uuid",
  "new_study_year": "2024-2025"
}
```

### 10. Bulk Class Upgrade (POST)
**Endpoint**: `POST /students/bulk-upgrade-class`

**Description**: Move all students from one class to another class.

**Request Body**:
```json
{
  "current_class_id": "old_class_uuid",
  "new_class_id": "new_class_uuid",
  "new_study_year": "2024-2025"
}
```

**Response**:
```json
{
  "message": "Successfully upgraded 35 students",
  "affected_students": 35
}
```

### 11. Delete Student
**Endpoint**: `DELETE /students/{student_id}`

---

## Buses

### 1. Create Bus
**Endpoint**: `POST /buses`

**Request Body**:
```json
{
  "registration_number": "TN01AB1234",
  "driver_id": "driver_uuid",
  "route_id": "route_uuid",
  "vehicle_type": "Mini Bus",
  "bus_brand": "Tata",
  "bus_model": "Starbus",
  "seating_capacity": 40,
  "rc_expiry_date": "2025-12-31",
  "fc_expiry_date": "2025-06-30",
  "rc_book_url": "https://example.com/rc.pdf",
  "fc_certificate_url": "https://example.com/fc.pdf"
}
```

### 2. Get All Buses
**Endpoint**: `GET /buses`

### 3. Get Bus by ID
**Endpoint**: `GET /buses/{bus_id}`

### 4. Update Bus
**Endpoint**: `PUT /buses/{bus_id}`

### 5. Update Bus Status (PUT)
**Endpoint**: `PUT /buses/{bus_id}/status`

**Request Body**:
```json
{
  "status": "ACTIVE"
}
```

### 6. Update Bus Status (PATCH)
**Endpoint**: `PATCH /buses/{bus_id}/status`

**Request Body**:
```json
{
  "status": "INACTIVE"
}
```

**Available Status Values**: `ACTIVE`, `INACTIVE`, `MAINTENANCE`

### 7. Assign Route to Bus (PATCH)
**Endpoint**: `PATCH /buses/{bus_id}/route`

**Request Body**:
```json
{
  "route_id": "route_uuid"
}
```

### 8. Update Bus Documents (PATCH)
**Endpoint**: `PATCH /buses/{bus_id}/documents`

**Request Body**:
```json
{
  "rc_book_url": "https://example.com/new_rc.pdf",
  "fc_certificate_url": "https://example.com/new_fc.pdf"
}
```

### 9. Delete Bus
**Endpoint**: `DELETE /buses/{bus_id}`

---

## Routes

### 1. Create Route
**Endpoint**: `POST /routes`

**Request Body**:
```json
{
  "name": "Route 1 - Anna Nagar to School"
}
```

### 2. Get All Routes
**Endpoint**: `GET /routes`

### 3. Get Route by ID
**Endpoint**: `GET /routes/{route_id}`

### 4. Update Route
**Endpoint**: `PUT /routes/{route_id}`

**Request Body**:
```json
{
  "name": "Updated Route Name",
  "routes_active_status": "ACTIVE"
}
```

### 5. Update Route Status
**Endpoint**: `PUT /routes/{route_id}/status`

**Request Body**:
```json
{
  "status": "ACTIVE"
}
```

### 6. Delete Route
**Endpoint**: `DELETE /routes/{route_id}`

---

## Route Stops

### 1. Create Route Stop
**Endpoint**: `POST /route-stops`

**Description**: Create a new route stop. The API validates the route, ensures the order is sequential (no gaps), shifts any existing stops to make room, and rebuilds the FCM cache.

**Request Body**:
```json
{
  "route_id": "route_uuid",
  "stop_name": "Anna Nagar Stop",
  "latitude": 13.0827,
  "longitude": 80.2707,
  "pickup_stop_order": 1,
  "drop_stop_order": 5
}
```

**Response**: Array of all route stops for that route, sorted by order.

### 2. Get All Route Stops
**Endpoint**: `GET /route-stops`

**Query Parameters** (optional):
- `route_id`: Filter by route ID

**Example**: `GET /route-stops?route_id=route_uuid`

### 3. Get Route Stop by ID
**Endpoint**: `GET /route-stops/{stop_id}`

### 4. Update Route Stop
**Endpoint**: `PUT /route-stops/{stop_id}`

### 5. Delete Route Stop
**Endpoint**: `DELETE /route-stops/{stop_id}`

---

## Classes

### 1. Create Class
**Endpoint**: `POST /classes`

**Request Body**:
```json
{
  "class_name": "10",
  "section": "A",
  "academic_year": "2024-2025"
}
```

### 2. Get All Classes
**Endpoint**: `GET /classes`

### 3. Get Class by ID
**Endpoint**: `GET /classes/{class_id}`

### 4. Update Class
**Endpoint**: `PUT /classes/{class_id}`

### 5. Update Class Status
**Endpoint**: `PUT /classes/{class_id}/status`

**Request Body**:
```json
{
  "status": "ACTIVE"
}
```

### 6. Delete Class
**Endpoint**: `DELETE /classes/{class_id}`

---

## Trips

### 1. Create Trip
**Endpoint**: `POST /trips`

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

**Trip Type Options**: `MORNING`, `EVENING`

### 2. Get All Trips
**Endpoint**: `GET /trips`

### 3. Get Trip by ID
**Endpoint**: `GET /trips/{trip_id}`

### 4. Update Trip
**Endpoint**: `PUT /trips/{trip_id}`

**Request Body**:
```json
{
  "status": "ONGOING",
  "current_stop_order": 3,
  "started_at": "2024-01-15T07:00:00",
  "ended_at": null
}
```

**Trip Status Options**: `NOT_STARTED`, `ONGOING`, `PAUSED`, `COMPLETED`, `CANCELED`

### 5. Update Trip Status (PUT)
**Endpoint**: `PUT /trips/{trip_id}/status`

**Request Body**:
```json
{
  "status": "COMPLETED"
}
```

### 6. Update Trip Status (PATCH)
**Endpoint**: `PATCH /trips/{trip_id}/status`

**Request Body**:
```json
{
  "status": "COMPLETED"
}
```

**Trip Status Options**: `NOT_STARTED`, `ONGOING`, `PAUSED`, `COMPLETED`, `CANCELED`

### 7. Delete Trip
**Endpoint**: `DELETE /trips/{trip_id}`

---

## Bus Tracking

### 1. Update Bus Location
**Endpoint**: `POST /bus-tracking/location`

**Request Body**:
```json
{
  "trip_id": "trip_uuid",
  "latitude": 13.0827,
  "longitude": 80.2707,
  "timestamp": "2024-01-15T07:30:00"
}
```

### 2. Get Current Bus Location
**Endpoint**: `GET /bus-tracking/{trip_id}/location`

### 3. Send Notification
**Endpoint**: `POST /bus-tracking/notify`

**Request Body**:
```json
{
  "trip_id": "trip_uuid",
  "message": "Bus arriving in 5 minutes",
  "stop_id": "stop_uuid"
}
```

---

## FCM Tokens

### 1. Create FCM Token
**Endpoint**: `POST /fcm-tokens`

**Request Body**:
```json
{
  "fcm_token": "firebase_token_here",
  "student_id": "student_uuid",
  "parent_id": "parent_uuid"
}
```

### 2. Get All FCM Tokens
**Endpoint**: `GET /fcm-tokens`

### 3. Get FCM Token by ID
**Endpoint**: `GET /fcm-tokens/{fcm_id}`

### 4. Update FCM Token
**Endpoint**: `PUT /fcm-tokens/{fcm_id}`

### 5. Delete FCM Token
**Endpoint**: `DELETE /fcm-tokens/{fcm_id}`

---

## Error Handling

### 1. Create Error Log
**Endpoint**: `POST /error-handling`

**Request Body**:
```json
{
  "error_type": "API_ERROR",
  "error_code": 500,
  "error_description": "Internal server error occurred"
}
```

### 2. Get All Error Logs
**Endpoint**: `GET /error-handling`

### 3. Get Error Log by ID
**Endpoint**: `GET /error-handling/{error_id}`

### 4. Update Error Log
**Endpoint**: `PUT /error-handling/{error_id}`

### 5. Delete Error Log
**Endpoint**: `DELETE /error-handling/{error_id}`

---

## Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

---

## Common Response Structures

### Success Response
```json
{
  "id": "uuid",
  "field1": "value1",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Error Response
```json
{
  "detail": "Error message here"
}
```

### List Response
```json
[
  {
    "id": "uuid1",
    "field": "value1"
  },
  {
    "id": "uuid2",
    "field": "value2"
  }
]
```

---

## Notes for Frontend Developers

1. **All IDs are UUIDs** (e.g., "550e8400-e29b-41d4-a716-446655440000")
2. **Phone numbers** must be 10 digits (e.g., 9876543210)
3. **Dates** format: "YYYY-MM-DD" (e.g., "2024-01-15")
4. **Timestamps** format: ISO 8601 (e.g., "2024-01-15T07:30:00")
5. **All endpoints** (except login and create admin) require JWT token
6. **Token expires** after a certain period - implement token refresh logic
7. **PATCH vs PUT**: Use PATCH for partial updates of specific fields, PUT for full updates

---

- **Base URL**: `https://api.selvagam.com/api/v1` (Production) / `http://72.61.250.191:8080/api/v1` (IP Backup)

## Interactive Documentation

For interactive API testing and more details, visit:
- **Swagger UI**: https://api.selvagam.com/docs
- **ReDoc**: https://api.selvagam.com/redoc

---

## Support

For API support, contact: admin@school.com
