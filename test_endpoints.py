#!/usr/bin/env python3

import sys
import traceback
from database import get_db

def test_parents_endpoint():
    """Test the parents GET endpoint logic"""
    try:
        print("Testing parents endpoint...")
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM parents ORDER BY created_at DESC")
                parents = cursor.fetchall()
                print(f"✓ Parents query successful - Found {len(parents)} records")
                if parents:
                    print(f"Sample parent: {parents[0]}")
                return parents
    except Exception as e:
        print(f"✗ Parents endpoint error: {str(e)}")
        traceback.print_exc()
        return None

def test_routes_endpoint():
    """Test the routes GET endpoint logic"""
    try:
        print("\nTesting routes endpoint...")
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM routes ORDER BY name")
                routes = cursor.fetchall()
                print(f"✓ Routes query successful - Found {len(routes)} records")
                if routes:
                    print(f"Sample route: {routes[0]}")
                return routes
    except Exception as e:
        print(f"✗ Routes endpoint error: {str(e)}")
        traceback.print_exc()
        return None

def test_database_connection():
    """Test basic database connectivity"""
    try:
        print("Testing database connection...")
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 as test")
                result = cursor.fetchone()
                print(f"✓ Database connection successful: {result}")
                return True
    except Exception as e:
        print(f"✗ Database connection error: {str(e)}")
        traceback.print_exc()
        return False

def check_table_structure():
    """Check if tables exist and have correct structure"""
    try:
        print("\nChecking table structure...")
        with get_db() as conn:
            with conn.cursor() as cursor:
                # Check parents table
                cursor.execute("SHOW TABLES LIKE 'parents'")
                if cursor.fetchone():
                    cursor.execute("DESCRIBE parents")
                    parents_cols = cursor.fetchall()
                    print(f"✓ Parents table exists with {len(parents_cols)} columns")
                else:
                    print("✗ Parents table does not exist")
                
                # Check routes table
                cursor.execute("SHOW TABLES LIKE 'routes'")
                if cursor.fetchone():
                    cursor.execute("DESCRIBE routes")
                    routes_cols = cursor.fetchall()
                    print(f"✓ Routes table exists with {len(routes_cols)} columns")
                else:
                    print("✗ Routes table does not exist")
                    
    except Exception as e:
        print(f"✗ Table structure check error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Testing School Transport API Endpoints ===")
    
    # Test database connection first
    if not test_database_connection():
        print("Database connection failed. Exiting...")
        sys.exit(1)
    
    # Check table structure
    check_table_structure()
    
    # Test endpoints
    test_parents_endpoint()
    test_routes_endpoint()
    
    print("\n=== Test Complete ===")