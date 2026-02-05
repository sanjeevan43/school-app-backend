# 🔧 Troubleshooting: Parent Creation 400 Error

## Problem
Getting 400 "Failed to create parent" error when trying to create a parent.

## Solutions

### 1. Check Database Connection
```bash
# Test database connection
mysql -h localhost -u root -p
USE school_DB;
SHOW TABLES;
```

### 2. Run Database Schema
```bash
# Import the database schema
mysql -h localhost -u root -p < database_schema.sql
```

### 3. Check Environment Variables
Create `.env` file from `.env.example`:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 4. Verify Database Table Structure
```sql
DESCRIBE parents;
```

### 5. Check Server Logs
Look for detailed error messages in the console where you're running:
```bash
python main.py
```

### 6. Test with Simple Data
Try creating a parent with minimal data:
```json
{
  "phone": 9876543210,
  "name": "Test Parent",
  "password": "test123"
}
```

### 7. Common Issues
- **Database not running**: Start MySQL service
- **Wrong credentials**: Check DB_USER, DB_PASSWORD in .env
- **Table doesn't exist**: Run database_schema.sql
- **Duplicate phone**: Phone number already exists
- **Missing required fields**: Ensure all required fields are provided

### 8. Quick Fix Commands
```bash
# 1. Create database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS school_DB;"

# 2. Import schema
mysql -u root -p school_DB < database_schema.sql

# 3. Check if parent table exists
mysql -u root -p -e "USE school_DB; SHOW TABLES LIKE 'parents';"
```

## Test Endpoint
After fixing, test with:
```bash
curl -X POST "http://localhost:8000/api/v1/parents" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": 9876543210,
    "name": "Test Parent",
    "password": "test123"
  }'
```