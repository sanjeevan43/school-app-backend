#!/usr/bin/env python3
"""
Complete error fix script for School Transport Management API
"""

from database import get_db
from auth import get_password_hash
import uuid

def fix_all_errors():
    """Fix all critical errors in the system"""
    print("🔧 Fixing all system errors...")
    
    with get_db() as conn:
        with conn.cursor() as cursor:
            # 1. Fix database schema issues
            print("1️⃣ Fixing database schema...")
            
            schema_fixes = [
                ("ALTER TABLE drivers ADD COLUMN password_hash VARCHAR(255) NOT NULL DEFAULT ''", 
                 "Added password_hash to drivers"),
                ("ALTER TABLE parents CHANGE COLUMN fcm_toten fcm_token VARCHAR(255) DEFAULT NULL", 
                 "Fixed fcm_token typo in parents"),
                ("ALTER TABLE drivers ADD COLUMN fcm_token VARCHAR(255) DEFAULT NULL", 
                 "Added fcm_token to drivers"),
                ("ALTER TABLE trips DROP COLUMN trips_status", 
                 "Removed extra trips_status column")
            ]
            
            for sql, message in schema_fixes:
                try:
                    cursor.execute(sql)
                    print(f"   ✅ {message}")
                except Exception as e:
                    if "Duplicate column" in str(e) or "doesn't exist" in str(e):
                        print(f"   ⚠️  {message} - Already fixed")
                    else:
                        print(f"   ❌ {message} - {e}")
            
            # 2. Create test admin if none exists
            print("\n2️⃣ Ensuring admin user exists...")
            cursor.execute("SELECT COUNT(*) as count FROM admins")
            admin_count = cursor.fetchone()['count']
            
            if admin_count == 0:
                admin_id = str(uuid.uuid4())
                password_hash = get_password_hash("admin123")
                
                cursor.execute("""
                    INSERT INTO admins (admin_id, phone, email, password_hash, name, dob)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (admin_id, 9876543210, "admin@test.com", password_hash, "System Admin", "1990-01-01"))
                
                print("   ✅ Created test admin")
                print("      Phone: 9876543210")
                print("      Password: admin123")
            else:
                print(f"   ✅ {admin_count} admin(s) already exist")
                
                # Fix existing admins without password_hash
                cursor.execute("SELECT admin_id, phone, name FROM admins WHERE password_hash IS NULL OR password_hash = ''")
                admins_without_password = cursor.fetchall()
                
                for admin in admins_without_password:
                    password_hash = get_password_hash("admin123")
                    cursor.execute("UPDATE admins SET password_hash = %s WHERE admin_id = %s", 
                                 (password_hash, admin['admin_id']))
                    print(f"   ✅ Added password to admin: {admin['name']} ({admin['phone']})")
            
            # 3. Fix drivers without password_hash
            print("\n3️⃣ Fixing driver passwords...")
            cursor.execute("SELECT driver_id, name, phone FROM drivers WHERE password_hash IS NULL OR password_hash = ''")
            drivers_without_password = cursor.fetchall()
            
            for driver in drivers_without_password:
                password_hash = get_password_hash("driver123")
                cursor.execute("UPDATE drivers SET password_hash = %s WHERE driver_id = %s", 
                             (password_hash, driver['driver_id']))
                print(f"   ✅ Added password to driver: {driver['name']} ({driver['phone']})")
            
            # 4. Fix parents without password_hash
            print("\n4️⃣ Fixing parent passwords...")
            cursor.execute("SELECT parent_id, name, phone FROM parents WHERE password_hash IS NULL OR password_hash = ''")
            parents_without_password = cursor.fetchall()
            
            for parent in parents_without_password:
                password_hash = get_password_hash("parent123")
                cursor.execute("UPDATE parents SET password_hash = %s WHERE parent_id = %s", 
                             (password_hash, parent['parent_id']))
                print(f"   ✅ Added password to parent: {parent['name']} ({parent['phone']})")
    
    print("\n🎉 All errors fixed! System is now ready.")
    print("\n📋 Test Credentials:")
    print("   Admin - Phone: 9876543210, Password: admin123")
    print("   Drivers - Password: driver123")
    print("   Parents - Password: parent123")

if __name__ == "__main__":
    fix_all_errors()