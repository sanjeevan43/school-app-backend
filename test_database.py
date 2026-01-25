#!/usr/bin/env python3
"""
Database Connection Test
Verifies database connection and basic table structure
"""

import pymysql
from config import get_settings
import sys

def test_database_connection():
    """Test database connection and basic operations"""
    settings = get_settings()
    
    print("Testing Database Connection...")
    print(f"Host: {settings.DB_HOST}")
    print(f"Port: {settings.DB_PORT}")
    print(f"Database: {settings.DB_NAME}")
    print(f"User: {settings.DB_USER}")
    print("-" * 50)
    
    try:
        # Test connection
        connection = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("Database connection successful!")
        
        with connection.cursor() as cursor:
            # Test basic query
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            print(f"Basic query test: {result}")
            
            # Check tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"Found {len(tables)} tables:")
            
            expected_tables = [
                'admins', 'parents', 'drivers', 'routes', 
                'buses', 'route_stops', 'students', 'trips'
            ]
            
            existing_tables = [table[f'Tables_in_{settings.DB_NAME}'] for table in tables]
            
            for table in expected_tables:
                if table in existing_tables:
                    print(f"   [OK] {table}")
                    
                    # Count records in each table
                    cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                    count = cursor.fetchone()['count']
                    print(f"      Records: {count}")
                else:
                    print(f"   [MISSING] {table}")
            
            # Test admin table structure
            print("\nAdmin table structure:")
            cursor.execute("DESCRIBE admins")
            columns = cursor.fetchall()
            for col in columns:
                print(f"   {col['Field']} - {col['Type']}")
        
        connection.close()
        print("\nDatabase test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

def main():
    """Main function"""
    print("School Transport Management - Database Test")
    print("=" * 50)
    
    success = test_database_connection()
    
    if success:
        print("\nDatabase is ready for API testing!")
        print("Run: python test_complete_api.py")
    else:
        print("\nPlease fix database connection issues before running API tests.")
        sys.exit(1)

if __name__ == "__main__":
    main()