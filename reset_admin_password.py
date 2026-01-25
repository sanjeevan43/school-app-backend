#!/usr/bin/env python3
"""
Reset admin password with new bcrypt implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from auth import get_password_hash

def reset_admin_password():
    """Reset admin password to ensure it works with new bcrypt"""
    
    phone = 9876543210
    new_password = "admin123"  # Simple password for testing
    
    try:
        # Hash the password with new implementation
        password_hash = get_password_hash(new_password)
        print(f"New password hash: {password_hash[:50]}...")
        
        # Update in database
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE admins SET password_hash = %s WHERE phone = %s",
                    (password_hash, phone)
                )
                
                if cursor.rowcount > 0:
                    print(f"SUCCESS: Password updated for admin with phone {phone}")
                    print(f"New login credentials:")
                    print(f"  Phone: {phone}")
                    print(f"  Password: {new_password}")
                else:
                    print("FAILED: No admin found with that phone number")
                    
                # Show all admins
                cursor.execute("SELECT phone, name, admin_id FROM admins")
                admins = cursor.fetchall()
                print(f"\nAll admins in database:")
                for admin in admins:
                    print(f"  Phone: {admin['phone']}, Name: {admin['name']}")
                    
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    reset_admin_password()