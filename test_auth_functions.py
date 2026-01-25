#!/usr/bin/env python3
"""
Test the auth.py functions directly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth import get_password_hash, verify_password

def test_auth_functions():
    """Test the auth functions directly"""
    
    password = "Rahul@12345"
    
    print(f"Testing password: {password}")
    print(f"Password length: {len(password)} characters")
    print(f"Password bytes: {len(password.encode('utf-8'))} bytes")
    
    try:
        # Test hashing
        hashed = get_password_hash(password)
        print(f"SUCCESS: Password hashed: {hashed[:50]}...")
        
        # Test verification
        verified = verify_password(password, hashed)
        print(f"Verification result: {verified}")
        
        # Test wrong password
        wrong_verified = verify_password("wrong_password", hashed)
        print(f"Wrong password verification: {wrong_verified}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    test_auth_functions()