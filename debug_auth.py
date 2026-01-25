#!/usr/bin/env python3
from database import get_db
from auth import verify_password

def debug_auth():
    print("🔍 Debugging Authentication...")
    
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                # Check database connection
                print("✅ Database connected")
                
                # Check admins table
                cursor.execute("SELECT COUNT(*) as count FROM admins")
                admin_count = cursor.fetchone()['count']
                print(f"📊 Admins in database: {admin_count}")
                
                if admin_count > 0:
                    # Show admin data
                    cursor.execute("SELECT phone, name, password_hash FROM admins LIMIT 3")
                    admins = cursor.fetchall()
                    
                    for admin in admins:
                        print(f"👤 Admin: {admin['name']}")
                        print(f"   📞 Phone: {admin['phone']}")
                        print(f"   🔐 Has Password: {'Yes' if admin['password_hash'] else 'No'}")
                        
                        # Test password verification
                        if admin['password_hash']:
                            test_passwords = ['admin123', 'password', '123456', 'admin']
                            for pwd in test_passwords:
                                if verify_password(pwd, admin['password_hash']):
                                    print(f"   ✅ Password found: {pwd}")
                                    break
                            else:
                                print("   ❌ Password not in common list")
                        print()
                
                # Check parents
                cursor.execute("SELECT COUNT(*) as count FROM parents")
                parent_count = cursor.fetchone()['count']
                print(f"📊 Parents in database: {parent_count}")
                
                # Check drivers  
                cursor.execute("SELECT COUNT(*) as count FROM drivers")
                driver_count = cursor.fetchone()['count']
                print(f"📊 Drivers in database: {driver_count}")
                
    except Exception as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    debug_auth()