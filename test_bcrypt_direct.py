#!/usr/bin/env python3
"""
Test bcrypt directly without passlib
"""

import bcrypt

def test_bcrypt_direct():
    """Test bcrypt directly"""
    
    password = "Rahul@12345"
    
    print(f"Password: {password}")
    print(f"Password length: {len(password)} characters")
    print(f"Password bytes: {len(password.encode('utf-8'))} bytes")
    
    try:
        # Convert to bytes
        password_bytes = password.encode('utf-8')
        
        # Generate salt and hash
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        print(f"SUCCESS: Hash created: {hashed}")
        
        # Verify
        verified = bcrypt.checkpw(password_bytes, hashed)
        print(f"Verification: {verified}")
        
        return hashed.decode('utf-8')
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    test_bcrypt_direct()