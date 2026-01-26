import uvicorn
import asyncio
import requests
import time
import threading
from main import app

def test_server():
    time.sleep(2)  # Wait for server to start
    try:
        response = requests.get("http://127.0.0.1:8080/api/v1/admins", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    # Start test in background
    test_thread = threading.Thread(target=test_server, daemon=True)
    test_thread.start()
    
    # Start server with logging
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")