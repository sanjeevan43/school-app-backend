#!/usr/bin/env python3
from database import get_db
from auth import get_password_hash
import uuid

def create_test_admin():
    with get_db() as conn:
        with conn.cursor() as cursor:
            # Check if admin exists
            cursor.execute("SELECT COUNT(*) as count FROM admins")
            count = cursor.fetchone()['count']
            
            if count == 0:
                print("No admin found. Creating test admin...")
                admin_id = str(uuid.uuid4())
                password_hash = get_password_hash("admin123")
                
                cursor.execute("""
                    INSERT INTO admins (admin_id, phone, email, password_hash, name, dob)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (admin_id, 9876543210, "admin@test.com", password_hash, "Test Admin", "1990-01-01"))
                
                print("✅ Admin created!")
                print("   Phone: 9876543210")
                print("   Password: admin123")
            else:
                print(f"✅ {count} admin(s) already exist")
                cursor.execute("SELECT phone, name FROM admins LIMIT 1")
                admin = cursor.fetchone()
                print(f"   Phone: {admin['phone']}")
                print(f"   Name: {admin['name']}")

if __name__ == "__main__":
    create_test_admin()