# 🧪 Test Your School API - Proper Commands

## ✅ Check Service Status
```bash
systemctl status school-api
```

## 🚀 Test Your School API Endpoints

### 1. Test Root Endpoint
```bash
curl http://72.62.196.30/
```

### 2. Test Swagger UI (Open in Browser)
```
http://72.62.196.30/docs
```

### 3. Create Admin (First Test)
```bash
curl -X POST "http://72.62.196.30/api/v1/admins" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": 9876543210,
    "email": "admin@school.com",
    "name": "School Admin",
    "password": "admin123",
    "dob": "1990-01-01"
  }'
```

### 4. Admin Login
```bash
curl -X POST "http://72.62.196.30/api/v1/auth/admin/login" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": 9876543210,
    "password": "admin123"
  }'
```

### 5. Test Get All Admins (with token)
```bash
# First get token from login, then:
curl -X GET "http://72.62.196.30/api/v1/admins" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 6. Send OTP Test
```bash
curl -X POST "http://72.62.196.30/api/v1/auth/send-otp" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": 9123456789,
    "user_type": "parent"
  }'
```

## 🌐 Your Live School API URLs:
- **Main API**: http://72.62.196.30/api/v1
- **Swagger UI**: http://72.62.196.30/docs
- **ReDoc**: http://72.62.196.30/redoc

## 📱 Quick API Test
```bash
# Test if API is responding
curl -I http://72.62.196.30/docs

# Test API root
curl http://72.62.196.30/

# Check if main API path works
curl http://72.62.196.30/api/v1/
```

## 🔧 If API Not Working, Check:
```bash
# Check if Python process is running
ps aux | grep uvicorn

# Check logs
journalctl -u school-api -f

# Manual start (for testing)
cd /var/www/selvagam_school_app
source venv/bin/activate
python main.py
```