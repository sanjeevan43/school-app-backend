from database import get_db_connection
from config import get_settings

def test_db_connection():
    try:
        settings = get_settings()
        print(f"Connecting to: {settings.DB_HOST}:{settings.DB_PORT}")
        print(f"Database: {settings.DB_NAME}")
        print(f"User: {settings.DB_USER}")
        
        conn = get_db_connection()
        print("✅ Database connection successful!")
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"MySQL Version: {version['VERSION()']}")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

if __name__ == "__main__":
    test_db_connection()