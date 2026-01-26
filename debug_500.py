import traceback
from database import get_db

def test_database():
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"Tables: {[list(t.values())[0] for t in tables]}")
                
                # Test each table
                for table in tables:
                    table_name = list(table.values())[0]
                    try:
                        cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                        count = cursor.fetchone()['count']
                        print(f"{table_name}: {count} records")
                    except Exception as e:
                        print(f"{table_name}: ERROR - {e}")
    except Exception as e:
        print(f"Database error: {e}")
        traceback.print_exc()

def test_routes():
    try:
        from routes import router
        print("Routes imported successfully")
    except Exception as e:
        print(f"Routes error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Testing Database ===")
    test_database()
    print("\n=== Testing Routes ===")
    test_routes()