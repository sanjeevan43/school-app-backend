#!/usr/bin/env python3
"""
Reset all user passwords to work with new bcrypt implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from auth import get_password_hash

def reset_all_passwords():
    """Reset passwords for all users"""
    
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                
                # Reset admin passwords
                print("Resetting admin passwords...")
                cursor.execute("SELECT admin_id, phone, name FROM admins")
                admins = cursor.fetchall()
                
                for admin in admins:
                    password = "admin123"
                    password_hash = get_password_hash(password)
                    cursor.execute(
                        "UPDATE admins SET password_hash = %s WHERE admin_id = %s",
                        (password_hash, admin['admin_id'])
                    )
                    print(f"  Admin {admin['name']} (Phone: {admin['phone']}) -> Password: {password}")
                
                # Reset parent passwords
                print("\\nResetting parent passwords...")
                cursor.execute("SELECT parent_id, phone, name FROM parents")
                parents = cursor.fetchall()
                
                for parent in parents:
                    password = "parent123"
                    password_hash = get_password_hash(password)
                    cursor.execute(
                        "UPDATE parents SET password_hash = %s WHERE parent_id = %s",
                        (password_hash, parent['parent_id'])
                    )
                    print(f"  Parent {parent['name']} (Phone: {parent['phone']}) -> Password: {password}")
                
                # Reset driver passwords
                print("\\nResetting driver passwords...")
                cursor.execute("SELECT driver_id, phone, name FROM drivers")
                drivers = cursor.fetchall()
                
                for driver in drivers:
                    password = "driver123"
                    password_hash = get_password_hash(password)
                    cursor.execute(
                        "UPDATE drivers SET password_hash = %s WHERE driver_id = %s",
                        (password_hash, driver['driver_id'])
                    )
                    print(f"  Driver {driver['name']} (Phone: {driver['phone']}) -> Password: {password}")
                
                print(f"\\nSUCCESS: Reset passwords for {len(admins)} admins, {len(parents)} parents, {len(drivers)} drivers")
                
                print("\\n=== LOGIN CREDENTIALS ===")
                print("Admins: password = 'admin123'")
                print("Parents: password = 'parent123'")
                print("Drivers: password = 'driver123'")
                
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    reset_all_passwords()