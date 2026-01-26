#!/usr/bin/env python3
"""
Comprehensive fix script for the School Transport Management API
"""

import sys
import os
import traceback
from datetime import datetime

def test_database_connection():
    """Test database connection"""
    try:
        from database import get_db
        print("[OK] Testing database connection...")
        
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 as test")
                result = cursor.fetchone()
                if result and result['test'] == 1:
                    print("[OK] Database connection successful")
                    return True
        return False
    except Exception as e:
        print(f"[FAIL] Database connection failed: {e}")
        return False

def test_imports():
    """Test all required imports"""
    try:
        print("[OK] Testing imports...")
        import fastapi
        import uvicorn
        import pymysql
        import jose
        import passlib
        import pydantic
        import cryptography
        import bcrypt
        from config import get_settings
        from models import AdminCreate, ParentCreate, DriverCreate
        from auth import get_password_hash, verify_password
        from encryption import encrypt_data, decrypt_data
        print("[OK] All imports successful")
        return True
    except Exception as e:
        print(f"[FAIL] Import failed: {e}")
        traceback.print_exc()
        return False

def test_password_hashing():
    """Test password hashing functionality"""
    try:
        print("[OK] Testing password hashing...")
        from auth import get_password_hash, verify_password
        
        test_password = "test123"
        hashed = get_password_hash(test_password)
        
        if verify_password(test_password, hashed):
            print("[OK] Password hashing works correctly")
            return True
        else:
            print("[FAIL] Password verification failed")
            return False
    except Exception as e:
        print(f"[FAIL] Password hashing failed: {e}")
        traceback.print_exc()
        return False

def test_encryption():
    """Test encryption functionality"""
    try:
        print("[OK] Testing encryption...")
        from encryption import encrypt_data, decrypt_data
        
        test_data = "Hello World"
        encrypted = encrypt_data(test_data)
        decrypted = decrypt_data(encrypted)
        
        if decrypted == test_data:
            print("[OK] Encryption/decryption works correctly")
            return True
        else:
            print("[FAIL] Encryption/decryption failed")
            return False
    except Exception as e:
        print(f"[FAIL] Encryption failed: {e}")
        traceback.print_exc()
        return False

def test_config():
    """Test configuration loading"""
    try:
        print("[OK] Testing configuration...")
        from config import get_settings
        
        settings = get_settings()
        required_fields = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'SECRET_KEY']
        
        for field in required_fields:
            if not hasattr(settings, field) or not getattr(settings, field):
                print(f"[FAIL] Missing or empty config field: {field}")
                return False
        
        print("[OK] Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Configuration failed: {e}")
        traceback.print_exc()
        return False

def test_models():
    """Test Pydantic models"""
    try:
        print("[OK] Testing Pydantic models...")
        from models import AdminCreate, ParentCreate, DriverCreate, LoginRequest
        
        # Test AdminCreate
        admin_data = {
            "phone": 9876543210,
            "email": "admin@test.com",
            "name": "Test Admin",
            "password": "admin123"
        }
        admin = AdminCreate(**admin_data)
        
        # Test LoginRequest
        login_data = {
            "phone": 9876543210,
            "password": "admin123"
        }
        login = LoginRequest(**login_data)
        
        print("[OK] Pydantic models work correctly")
        return True
    except Exception as e:
        print(f"[FAIL] Pydantic models failed: {e}")
        traceback.print_exc()
        return False

def check_database_tables():
    """Check if all required database tables exist"""
    try:
        print("[OK] Checking database tables...")
        from database import get_db
        
        required_tables = [
            'admins', 'parents', 'drivers', 'routes', 
            'buses', 'route_stops', 'students', 'trips'
        ]
        
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                existing_tables = [table[list(table.keys())[0]] for table in cursor.fetchall()]
                
                missing_tables = []
                for table in required_tables:
                    if table not in existing_tables:
                        missing_tables.append(table)
                
                if missing_tables:
                    print(f"[FAIL] Missing database tables: {missing_tables}")
                    return False
                else:
                    print("[OK] All required database tables exist")
                    return True
    except Exception as e:
        print(f"[FAIL] Database table check failed: {e}")
        return False

def test_api_startup():
    """Test if the API can start without errors"""
    try:
        print("[OK] Testing API startup...")
        from main import app
        
        # Try to access the OpenAPI schema (this will trigger any import/startup errors)
        schema = app.openapi()
        if schema and 'info' in schema:
            print("[OK] API startup successful")
            return True
        else:
            print("[FAIL] API startup failed - invalid schema")
            return False
    except Exception as e:
        print(f"[FAIL] API startup failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("School Transport Management API - Comprehensive Fix Check")
    print("=" * 60)
    print(f"Started at: {datetime.now()}")
    print()
    
    tests = [
        ("Configuration", test_config),
        ("Imports", test_imports),
        ("Password Hashing", test_password_hashing),
        ("Encryption", test_encryption),
        ("Pydantic Models", test_models),
        ("Database Connection", test_database_connection),
        ("Database Tables", check_database_tables),
        ("API Startup", test_api_startup),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[FAIL] {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {len(results)} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n[SUCCESS] All tests passed! Your API is ready to run.")
        print("\nTo start the API:")
        print("python main.py")
        print("\nOr with uvicorn:")
        print("uvicorn main:app --host 127.0.0.1 --port 8080 --reload")
    else:
        print(f"\n[WARNING] {failed} test(s) failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())