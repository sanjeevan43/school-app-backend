import sys
import traceback

def test_specific_endpoint():
    try:
        from database import get_db
        from models import AdminResponse
        
        print("Testing admin endpoint logic...")
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM admins ORDER BY created_at DESC")
                result = cursor.fetchall()
                print(f"Raw result: {result}")
                
                # Test if result can be serialized
                if result:
                    admin = result[0]
                    print(f"First admin: {admin}")
                    
                    # Check for None values that might cause issues
                    for key, value in admin.items():
                        if value is None:
                            print(f"NULL field: {key}")
                
                return result if result else []
                
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return None

def test_pydantic_model():
    try:
        from models import AdminResponse
        from database import get_db
        
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM admins LIMIT 1")
                admin_data = cursor.fetchone()
                
                if admin_data:
                    print(f"Admin data: {admin_data}")
                    # Try to create AdminResponse
                    admin_response = AdminResponse(**admin_data)
                    print("AdminResponse created successfully")
                else:
                    print("No admin data found")
                    
    except Exception as e:
        print(f"Pydantic error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Testing Endpoint Logic ===")
    test_specific_endpoint()
    print("\n=== Testing Pydantic Model ===")
    test_pydantic_model()