#!/usr/bin/env python3
"""
Simple API startup verification
"""

def main():
    try:
        print("Testing API startup...")
        
        # Import main components
        from main import app
        from config import get_settings
        
        settings = get_settings()
        
        print(f"[OK] API configured to run on {settings.API_HOST}:{settings.API_PORT}")
        print(f"[OK] Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
        print(f"[OK] Debug mode: {settings.DEBUG}")
        
        # Test OpenAPI schema generation
        schema = app.openapi()
        if schema and 'info' in schema:
            print(f"[OK] API Title: {schema['info']['title']}")
            print(f"[OK] API Version: {schema['info']['version']}")
            
            # Count endpoints
            paths = schema.get('paths', {})
            endpoint_count = sum(len(methods) for methods in paths.values())
            print(f"[OK] Total endpoints: {endpoint_count}")
        
        print("\n" + "="*50)
        print("API STARTUP VERIFICATION SUCCESSFUL")
        print("="*50)
        print("\nTo start your API, run:")
        print("python main.py")
        print("\nOr with uvicorn:")
        print(f"uvicorn main:app --host {settings.API_HOST} --port {settings.API_PORT} --reload")
        print(f"\nAPI will be available at: http://{settings.API_HOST}:{settings.API_PORT}")
        print(f"Documentation: http://{settings.API_HOST}:{settings.API_PORT}/docs")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] API startup verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)