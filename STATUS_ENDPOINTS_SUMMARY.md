## ✅ All Status Update Endpoints Added

### 🔄 Status Update Endpoints (PUT)
All tables now have dedicated status update endpoints:

1. **PUT /api/v1/admins/{admin_id}/status**
   - Body: `{"status": "ACTIVE" | "INACTIVE"}`

2. **PUT /api/v1/parents/{parent_id}/status**
   - Body: `{"status": "ACTIVE" | "INACTIVE"}`

3. **PUT /api/v1/drivers/{driver_id}/status**
   - Body: `{"status": "ACTIVE" | "INACTIVE"}`

4. **PUT /api/v1/routes/{route_id}/status**
   - Body: `{"status": "ACTIVE" | "INACTIVE"}`

5. **PUT /api/v1/buses/{bus_id}/status**
   - Body: `{"status": "ACTIVE" | "INACTIVE"}`

6. **PUT /api/v1/students/{student_id}/status**
   - Body: `{"status": "ACTIVE" | "TEMP_STOP" | "CANCELLED"}`

7. **PUT /api/v1/classes/{class_id}/status**
   - Body: `{"status": "ACTIVE" | "INACTIVE"}`

8. **PUT /api/v1/trips/{trip_id}/status**
   - Body: `{"status": "NOT_STARTED" | "ONGOING" | "PAUSED" | "COMPLETED" | "CANCELED"}`

### 📱 FCM Token Update for Parents
**PUT /api/v1/parents/{parent_id}/fcm-token**
- Body: `{"fcm_token": "your_fcm_token_here"}`
- Used when parent logs in to update their FCM token
- Automatically updates route FCM cache for parent's students

### 🎯 Usage Examples

```bash
# Update admin status
curl -X PUT "http://localhost:8000/api/v1/admins/admin-123/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "INACTIVE"}'

# Update student transport status
curl -X PUT "http://localhost:8000/api/v1/students/student-456/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "TEMP_STOP"}'

# Update parent FCM token on login
curl -X PUT "http://localhost:8000/api/v1/parents/parent-789/fcm-token" \
  -H "Content-Type: application/json" \
  -d '{"fcm_token": "fcm_token_string_here"}'
```

### ✨ Features
- **Minimal JSON**: Only status field required
- **Automatic Updates**: FCM cache updates automatically
- **Cascade Effects**: Status changes trigger related updates
- **ID Fields First**: All responses show ID fields first
- **Proper Validation**: Uses enum validation for status values

All endpoints are ready and working! 🚀