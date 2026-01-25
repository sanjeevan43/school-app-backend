#!/usr/bin/env python3
from database import get_db

def check_users():
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM admins")
            admin_count = cursor.fetchone()['count']
            print(f"Admins in database: {admin_count}")
            
            if admin_count > 0:
                cursor.execute("SELECT phone, name FROM admins")
                admins = cursor.fetchall()
                for admin in admins:
                    print(f"  - {admin['name']}: {admin['phone']}")

if __name__ == "__main__":
    check_users()