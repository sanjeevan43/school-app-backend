# 📊 Sample Test Data for API Testing

Copy and paste these JSON examples directly into Swagger UI:

## 🔐 Authentication Data

### Admin Login
```json
{
  "phone": 9876543210,
  "password": "admin123"
}
```

### OTP Request
```json
{
  "phone": 9123456789,
  "user_type": "parent"
}
```

### OTP Verify
```json
{
  "phone": 9123456789,
  "otp": "123456",
  "user_type": "parent"
}
```

## 👨💼 Admin Data

### Create Admin
```json
{
  "phone": 9876543210,
  "email": "admin@school.com",
  "name": "School Admin",
  "password": "admin123",
  "dob": "1985-01-15"
}
```

### Update Admin
```json
{
  "name": "Updated Admin Name",
  "email": "newadmin@school.com"
}
```

## 👨👩👧👦 Parent Data

### Create Parent
```json
{
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
  "emergency_contact": 9876543210
}
```

## 🚗 Driver Data

### Create Driver
```json
{
  "name": "Rajesh Kumar",
  "phone": 9987654321,
  "email": "driver@gmail.com",
  "dob": "1980-07-10",
  "licence_number": "MH01DL123456",
  "licence_expiry": "2025-12-31",
  "aadhar_number": "123456789012"
}
```

## 🛣️ Route Data

### Create Route
```json
{
  "name": "Route A - Central Mumbai"
}
```

### Create Route Stop
```json
{
  "route_id": "ROUTE_ID_FROM_RESPONSE",
  "stop_name": "Main Gate",
  "latitude": 19.0760,
  "longitude": 72.8777,
  "stop_order": 1
}
```

## 🚌 Bus Data

### Create Bus
```json
{
  "bus_number": "MH01AB1234",
  "bus_type": "AC",
  "bus_brand": "Tata",
  "bus_model": "Starbus",
  "seating_capacity": 40,
  "rc_expiry_date": "2025-06-30",
  "fc_expiry_date": "2024-12-31"
}
```

## 🎓 Student Data

### Create Student
```json
{
  "parent_id": "PARENT_ID_FROM_RESPONSE",
  "name": "Aarav Sharma",
  "dob": "2010-09-15",
  "class_section": "5th A",
  "route_id": "ROUTE_ID_FROM_RESPONSE",
  "pickup_stop_id": "STOP_ID_FROM_RESPONSE",
  "drop_stop_id": "STOP_ID_FROM_RESPONSE"
}
```

## 🚌 Trip Data

### Create Trip
```json
{
  "bus_id": "BUS_ID_FROM_RESPONSE",
  "driver_id": "DRIVER_ID_FROM_RESPONSE",
  "route_id": "ROUTE_ID_FROM_RESPONSE",
  "trip_date": "2024-01-15",
  "trip_type": "MORNING"
}
```

## 🔄 Testing Workflow

### 1. **Setup Phase**
```
1. Create Admin → Get admin_id
2. Login Admin → Get access_token
3. Authorize in Swagger with Bearer token
```

### 2. **Create Entities**
```
1. Create Parent → Get parent_id
2. Create Driver → Get driver_id  
3. Create Route → Get route_id
4. Create Route Stop → Get stop_id
5. Create Bus → Get bus_id
6. Create Student (use parent_id, route_id, stop_id)
7. Create Trip (use bus_id, driver_id, route_id)
```

### 3. **Test Operations**
```
1. GET all entities
2. GET by ID
3. UPDATE entities
4. DELETE entities
```

## 💡 **Pro Tips**

- **Copy UUIDs**: Always copy the IDs from responses to use in other requests
- **Use Variables**: Replace placeholder IDs with actual UUIDs from responses
- **Test Order**: Create dependencies first (Parent before Student)
- **Authorization**: Don't forget to authorize with Bearer token for protected endpoints

**Ready to test your API!** 🚀