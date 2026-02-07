# API Fixes Summary - 2026-02-07

## Issues Fixed

### 1. ✅ Driver Status - SUSPENDED Support
**Status:** COMPLETED

**Changes Made:**
- Added `DriverStatus` enum with values: `ACTIVE`, `INACTIVE`, `SUSPENDED`
- Created new `DriverStatusUpdate` Pydantic model in `models.py`
- Updated `PUT /api/v1/drivers/{driver_id}/status` endpoint to use `DriverStatusUpdate`

**How to Use:**
```json
PUT /api/v1/drivers/{driver_id}/status
{
  "status": "SUSPENDED"
}
```

**Available Status Values:**
- `ACTIVE` - Driver is active and available
- `INACTIVE` - Driver is inactive
- `SUSPENDED` - Driver is suspended (NEW)

---

### 2. ✅ Bus Status - MAINTENANCE Support
**Status:** COMPLETED

**Changes Made:**
- Added `BusStatus` enum with values: `ACTIVE`, `INACTIVE`, `MAINTENANCE`
- Created new `BusStatusUpdate` Pydantic model in `models.py`
- Updated `PUT /api/v1/buses/{bus_id}/status` endpoint to use `BusStatusUpdate`
- Updated `PATCH /api/v1/buses/{bus_id}/status` endpoint to use `BusStatusUpdate`

**How to Use:**
```json
PUT /api/v1/buses/{bus_id}/status
{
  "status": "MAINTENANCE"
}
```

**Available Status Values:**
- `ACTIVE` - Bus is active and operational
- `INACTIVE` - Bus is inactive
- `MAINTENANCE` - Bus is under maintenance (NEW)

---

### 3. ✅ Student Creation Error - Better Error Messages
**Status:** COMPLETED

**Problem:**
- Generic "Failed to create student" error message didn't help identify the actual issue
- Foreign key constraint violations weren't being reported clearly

**Changes Made:**
- Enhanced error handling in `POST /api/v1/students` endpoint
- Added specific error messages for each type of constraint violation:
  - Invalid `parent_id` - "Invalid parent_id: Parent not found"
  - Invalid `class_id` - "Invalid class_id: Class not found"
  - Invalid `pickup_route_id` - "Invalid pickup_route_id: Route not found"
  - Invalid `drop_route_id` - "Invalid drop_route_id: Route not found"
  - Invalid `pickup_stop_id` - "Invalid pickup_stop_id: Stop not found or doesn't belong to the pickup route"
  - Invalid `drop_stop_id` - "Invalid drop_stop_id: Stop not found or doesn't belong to the drop route"

**How It Helps:**
Now when creating a student fails, you'll get a specific error message indicating exactly which field has an invalid reference, making debugging much easier.

---

## Common Issues and Solutions

### Issue: "Invalid pickup_stop_id: Stop not found or doesn't belong to the pickup route"

**Cause:** The `pickup_stop_id` you're using either:
1. Doesn't exist in the `route_stops` table, OR
2. Exists but is associated with a different route than `pickup_route_id`

**Solution:**
1. First, verify the stop exists:
   ```
   GET /api/v1/route-stops/{pickup_stop_id}
   ```

2. Check that the stop's `route_id` matches your `pickup_route_id`:
   ```
   GET /api/v1/route-stops?route_id={pickup_route_id}
   ```

3. Use a stop_id from the list of stops that belong to the pickup route

**Example:**
If you want to create a student with:
- `pickup_route_id`: `"e139fd3e-de11-42cc-9ef9-6cd60c2e4ec7"`
- `drop_route_id`: `"e139fd3e-de11-42cc-9ef9-6cd60c2e4ec7"` (same route)

You must use stops that belong to this route. First, get the available stops:
```
GET /api/v1/route-stops?route_id=e139fd3e-de11-42cc-9ef9-6cd60c2e4ec7
```

Then use stop IDs from the response for both `pickup_stop_id` and `drop_stop_id`.

---

### Issue: Same Pickup and Drop Stop

**Note:** The API currently allows the same stop for both pickup and drop. This is valid for students who use the same location for both pickup and drop-off (e.g., home address is the same).

If you still get a validation error about "Pickup and drop stops must be different", this might be a custom validation in your frontend or a database constraint. Check:

1. Database constraints:
   ```sql
   SHOW CREATE TABLE students;
   ```

2. Frontend validation in your mobile/web app

---

## Testing the Fixes

### Test 1: Driver Suspended Status
```bash
# Create a driver
POST /api/v1/drivers
{
  "name": "Test Driver",
  "phone": 9999999999,
  "email": "test@example.com",
  "password": "test123",
  "licence_number": "DL123456",
  "licence_expiry": "2025-12-31"
}

# Update driver to SUSPENDED
PUT /api/v1/drivers/{driver_id}/status
{
  "status": "SUSPENDED"
}
```

### Test 2: Bus Maintenance Status
```bash
# Create a bus
POST /api/v1/buses
{
  "registration_number": "MH01TEST1234",
  "seating_capacity": 40,
  "vehicle_type": "AC"
}

# Update bus to MAINTENANCE
PUT /api/v1/buses/{bus_id}/status
{
  "status": "MAINTENANCE"
}
```

### Test 3: Student Creation with Better Errors
```bash
# Try creating student with invalid parent_id
POST /api/v1/students
{
  "parent_id": "invalid-parent-id",
  "name": "Test Student",
  "pickup_route_id": "valid-route-id",
  "drop_route_id": "valid-route-id",
  "pickup_stop_id": "valid-stop-id",
  "drop_stop_id": "valid-stop-id"
}

# Expected response: 400 Bad Request
# "Invalid parent_id: Parent not found"
```

---

## Files Modified

1. **models.py**
   - Added `DriverStatusUpdate` class
   - Added `BusStatusUpdate` class

2. **routes.py**
   - Updated `update_driver_status()` function
   - Updated `update_bus_status()` function (PUT)
   - Updated `patch_bus_status()` function (PATCH)
   - Enhanced `create_student()` error handling

---

## Database Schema Support

The database schema already supports these new status values:
- `drivers.status` - VARCHAR(20) - accepts ACTIVE, INACTIVE, SUSPENDED
- `buses.status` - VARCHAR(20) - accepts ACTIVE, INACTIVE, MAINTENANCE

No database migrations are required.

---

## API Documentation Update

The Swagger/OpenAPI documentation will automatically update with:
1. New status enum values for drivers (SUSPENDED)
2. New status enum values for buses (MAINTENANCE)
3. Better error response documentation for student creation

Access the updated docs at: `http://your-api-url/docs`

---

## Summary

All requested features have been implemented:
- ✅ Driver status now supports SUSPENDED
- ✅ Bus status now supports MAINTENANCE
- ✅ Student creation errors are now specific and helpful

The API is ready for deployment and testing.
