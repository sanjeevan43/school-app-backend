#!/usr/bin/env python3
"""
Quick API startup test
"""

import sys
import time
import threading
import requests
from main import app
import uvicorn

def test_api_endpoints():
    """Test basic API endpoints"""
    time.sleep(2)  # Wait for server to start
    
    try:
        # Test root endpoint
        response = requests.get("http://127.0.0.1:8080/", timeout=5)
        if response.status_code == 200:
            print("[OK] Root endpoint working")
        else:
            print(f"[FAIL] Root endpoint returned {response.status_code}")
            
        # Test health endpoint
        response = requests.get("http://127.0.0.1:8080/health", timeout=5)
        if response.status_code == 200:
            print("[OK] Health endpoint working")
        else:
            print(f"[FAIL] Health endpoint returned {response.status_code}")
            
        # Test docs endpoint
        response = requests.get("http://127.0.0.1:8080/docs", timeout=5)
        if response.status_code == 200:
            print("[OK] Swagger docs working")
        else:
            print(f"[FAIL] Swagger docs returned {response.status_code}")
            
        print("\n[SUCCESS] API is working correctly!")
        print("Access your API at: http://127.0.0.1:8080")
        print("API Documentation: http://127.0.0.1:8080/docs")
        
    except requests.exceptions.RequestException as e:
        print(f"[FAIL] API test failed: {e}")
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")

def run_server():
    """Run the server in a separate thread"""
    try:
        uvicorn.run(app, host="127.0.0.1", port=8080, log_level="error")
    except Exception as e:
        print(f"[FAIL] Server failed to start: {e}")

if __name__ == "__main__":
    print("Starting API server test...")
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Test endpoints
    test_api_endpoints()
    
    print("\nPress Ctrl+C to stop the server")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)