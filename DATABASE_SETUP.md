# Database Setup for Existing Database

## Update your .env file with your database credentials:

```env
# Your existing database credentials
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database_name
SECRET_KEY=your-secret-key
```

## Test database connection:

```bash
python -c "from database import get_db; print('✅ Database connected!' if get_db() else '❌ Connection failed')"
```

## Your API will now:
- ✅ Connect to your existing database
- ✅ Read data from your tables
- ✅ Insert/Update data to your tables
- ✅ Use your existing table structure

## Start the API:
```bash
python main.py
```

Your API endpoints will work with your existing database tables!