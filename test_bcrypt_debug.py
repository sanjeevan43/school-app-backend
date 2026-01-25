#!/usr/bin/env python3
"""
Debug bcrypt password hashing issue
"""

from passlib.context import CryptContext

def test_bcrypt_directly():
    """Test bcrypt directly with the problematic password"""
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password = "Rahul@12345"
    
    print(f"Password: {password}")
    print(f"Password length: {len(password)} characters")
    print(f"Password bytes: {len(password.encode('utf-8'))} bytes")
    
    try:
        # Test direct hashing
        hashed = pwd_context.hash(password)
        print(f"SUCCESS: Direct hash worked: {hashed[:50]}...")
        
        # Test verification
        verified = pwd_context.verify(password, hashed)
        print(f"Verification result: {verified}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        
        # Try with truncation
        print("\\nTrying with truncation...")
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            truncated_password = password_bytes[:72].decode('utf-8', errors='ignore')
        else:
            truncated_password = password
            
        print(f"Truncated password: {truncated_password}")
        print(f"Truncated length: {len(truncated_password)} characters")
        print(f"Truncated bytes: {len(truncated_password.encode('utf-8'))} bytes")
        
        try:
            hashed = pwd_context.hash(truncated_password)
            print(f"SUCCESS: Truncated hash worked: {hashed[:50]}...")
        except Exception as e2:
            print(f"ERROR with truncation: {e2}")

if __name__ == "__main__":
    test_bcrypt_directly()