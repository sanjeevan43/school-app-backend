#!/usr/bin/env python3
from database import get_db
from auth import get_password_hash

def fix_existing_admin():
    with get_db() as conn:
        with conn.cursor() as cursor:
            # Get first admin
            cursor.execute("SELECT admin_id, phone, name FROM admins LIMIT 1")
            admin = cursor.fetchone()
            
            if admin:
                # Add password hash
                password_hash = get_password_hash("admin123")
                cursor.execute("UPDATE admins SET password_hash = %s WHERE admin_id = %s", 
                             (password_hash, admin['admin_id']))
                
                print(f"✅ Updated admin: {admin['name']}")
                print(f"   Phone: {admin['phone']}")
                print(f"   Password: admin123")
            else:
                print("❌ No admin found")

if __name__ == "__main__":
    fix_existing_admin()