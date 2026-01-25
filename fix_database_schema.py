#!/usr/bin/env python3
"""
Database schema fix script - Run this to fix all database issues
"""

from database import get_db

def fix_database_schema():
    """Fix all database schema issues"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            fixes = [
                # Add password_hash to drivers
                ("ALTER TABLE drivers ADD COLUMN password_hash VARCHAR(255) NOT NULL DEFAULT ''", 
                 "Added password_hash to drivers"),
                
                # Fix fcm_token typo in parents
                ("ALTER TABLE parents CHANGE COLUMN fcm_toten fcm_token VARCHAR(255) DEFAULT NULL", 
                 "Fixed fcm_token typo in parents"),
                
                # Add fcm_token to drivers
                ("ALTER TABLE drivers ADD COLUMN fcm_token VARCHAR(255) DEFAULT NULL", 
                 "Added fcm_token to drivers"),
                
                # Remove extra trips_status column
                ("ALTER TABLE trips DROP COLUMN trips_status", 
                 "Removed extra trips_status column")
            ]
            
            for sql, message in fixes:
                try:
                    cursor.execute(sql)
                    print(f"✅ {message}")
                except Exception as e:
                    if "Duplicate column" in str(e) or "doesn't exist" in str(e):
                        print(f"⚠️  {message} - Already fixed or doesn't exist")
                    else:
                        print(f"❌ Error: {message} - {e}")

if __name__ == "__main__":
    print("Fixing database schema issues...")
    fix_database_schema()
    print("Schema fix completed!")