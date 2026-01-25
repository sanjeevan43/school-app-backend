#!/usr/bin/env python3
"""
Database health check and automatic fallback
"""

import pymysql
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_database_health():
    """Check if database is accessible"""
    try:
        connection = pymysql.connect(
            host="72.62.196.30",
            port=3306,
            user="myuser",
            password="Hope3Services@2026",
            database="school_DB",
            connect_timeout=10
        )
        connection.close()
        return True, "Remote database is accessible"
    except Exception as e:
        return False, f"Remote database error: {e}"

def switch_to_local():
    """Switch to local database configuration"""
    env_content = """# Local fallback configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_local_password
DB_NAME=school_DB
SECRET_KEY=selvagam-school-transport-secret-key-2024
API_HOST=127.0.0.1
API_PORT=8080
DEBUG=True"""
    
    with open('.env.backup', 'w') as f:
        f.write(env_content)
    
    print("Created .env.backup with local configuration")
    print("To switch: copy .env.backup to .env")

if __name__ == "__main__":
    is_healthy, message = check_database_health()
    print(f"Database Status: {message}")
    
    if not is_healthy:
        print("\n🔴 Remote database is down!")
        print("Options:")
        print("1. Wait for remote server to come back online")
        print("2. Switch to local MySQL database")
        print("3. Use SQLite for development")
        
        switch_to_local()
        
        print("\nTo use local database:")
        print("1. Install MySQL locally")
        print("2. Create 'school_DB' database")
        print("3. Copy .env.backup to .env")
        print("4. Update DB_PASSWORD in .env")
    else:
        print("✅ Remote database is working fine")