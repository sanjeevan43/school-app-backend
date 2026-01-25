#!/usr/bin/env python3
"""
Test database connection
"""

import pymysql
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import get_settings

def test_db_connection():
    """Test database connection"""
    settings = get_settings()
    
    print(f"Testing connection to: {settings.DB_HOST}:{settings.DB_PORT}")
    print(f"Database: {settings.DB_NAME}")
    print(f"User: {settings.DB_USER}")
    
    try:
        connection = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            connect_timeout=10
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        connection.close()
        print("SUCCESS: Database connection working!")
        return True
        
    except Exception as e:
        print(f"FAILED: {e}")
        return False

if __name__ == "__main__":
    test_db_connection()