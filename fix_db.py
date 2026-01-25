#!/usr/bin/env python3
from database import get_db

def fix_database():
    with get_db() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute("ALTER TABLE drivers ADD COLUMN password_hash VARCHAR(255) NOT NULL DEFAULT ''")
                print("✅ Added password_hash to drivers")
            except: pass
            
            try:
                cursor.execute("ALTER TABLE parents CHANGE COLUMN fcm_toten fcm_token VARCHAR(255) DEFAULT NULL")
                print("✅ Fixed fcm_token typo in parents")
            except: pass
            
            try:
                cursor.execute("ALTER TABLE drivers ADD COLUMN fcm_token VARCHAR(255) DEFAULT NULL")
                print("✅ Added fcm_token to drivers")
            except: pass
            
            try:
                cursor.execute("ALTER TABLE trips DROP COLUMN trips_status")
                print("✅ Removed extra trips_status column")
            except: pass

if __name__ == "__main__":
    fix_database()
    print("Database fixed!")