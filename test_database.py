#!/usr/bin/env python3
"""
Simple database test script
Run this to check if your database is working
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import execute_query, get_db
from config import get_settings

def test_database():
    """Test database connection and tables"""
    try:
        print("Testing database connection...")
        
        # Test basic connection
        with get_db() as conn:
            print("✅ Database connection successful")
        
        # Test if parents table exists
        result = execute_query("SHOW TABLES LIKE 'parents'", fetch_one=True)
        if result:
            print("✅ Parents table exists")
        else:
            print("❌ Parents table does not exist")
            print("Run: mysql -u root -p < database_schema.sql")
            return False
        
        # Test table structure
        result = execute_query("DESCRIBE parents", fetch_all=True)
        print(f"✅ Parents table has {len(result)} columns")
        
        # Test simple insert
        import uuid
        test_id = str(uuid.uuid4())
        query = """
        INSERT INTO parents (parent_id, phone, email, password_hash, name, parent_role)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (test_id, 1234567890, "test@test.com", "testpass", "Test Parent", "GUARDIAN"))
        print("✅ Test insert successful")
        
        # Clean up test data
        execute_query("DELETE FROM parents WHERE parent_id = %s", (test_id,))
        print("✅ Test cleanup successful")
        
        print("\n🎉 Database is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        print("\nTroubleshooting steps:")
        print("1. Make sure MySQL is running")
        print("2. Check your .env file has correct database credentials")
        print("3. Run: mysql -u root -p < database_schema.sql")
        return False

if __name__ == "__main__":
    test_database()