import os
import json
import time
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException, Request, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, messaging

app = FastAPI()

# Configuration
PORT = 8082
ADMIN_KEY = 'selvagam-admin-key-2024'

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Resolve Credentials Path Absolute
current_dir = Path(__file__).parent
possible_paths = [
    current_dir.parent / 'firebase-credentials.json',
    current_dir / 'firebase-credentials.json',
    Path(os.getcwd()) / 'firebase-credentials.json',
    Path('./firebase-credentials.json')
]

creds_path = next((p for p in possible_paths if p.exists()), None)

# 2. Initialize Firebase
def init_firebase():
    global creds_path
    try:
        if not creds_path:
            print(f'❌ CRITICAL: firebase-credentials.json NOT FOUND in paths: {[str(p) for p in possible_paths]}')
            return

        with open(creds_path, 'r', encoding='utf-8') as f:
            service_account = json.load(f)
        
        print('📁 Using Credentials File:', creds_path)

        # Force set Project ID for all Google SDKs
        project_id = service_account.get('project_id')
        if project_id:
            os.environ['GOOGLE_CLOUD_PROJECT'] = project_id
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(creds_path)
            print('🆔 Set Project ID:', project_id)

        # Check if already initialized
        try:
            firebase_apps = firebase_admin._apps
            if firebase_apps:
                print('🔄 Re-initializing Firebase...')
                for app_name in list(firebase_apps.keys()):
                    firebase_admin.delete_app(firebase_admin.get_app(app_name))
        except Exception as e:
            print(f'⚠️ Error during app cleanup: {e}')

        cred = credentials.Certificate(service_account)
        firebase_admin.initialize_app(cred, {
            'projectId': project_id
        })

        print('✅ Firebase Admin initialized for:', firebase_admin.get_app().project_id)
    except Exception as error:
        print('❌ Firebase Error during init:', str(error))

# Initialize at startup
init_firebase()

# Test endpoint
@app.get('/')
async def root():
    project_id = 'MISSING'
    try:
        project_id = firebase_admin.get_app().project_id
    except Exception:
        pass
    return {
        'message': 'FCM HTTP v1 API Server Running (Python)',
        'project': project_id,
        'status': 'Ready to send notifications'
    }

# Diagnostic Route
@app.get('/api/debug-status')
async def debug_status():
    project_id = 'MISSING'
    try:
        project_id = firebase_admin.get_app().project_id
    except Exception:
        pass
        
    return {
        'status': 'online',
        'projectId': project_id,
        'credsFound': creds_path is not None,
        'credsPath': str(creds_path) if creds_path else None,
        'envProject': os.environ.get('GOOGLE_CLOUD_PROJECT')
    }

# Authentication check
async def verify_api_key(x_admin_key: Optional[str] = Header(None)):
    if not x_admin_key or x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return x_admin_key

# Send to topic (broadcast) - Matches original server.js
@app.post('/api/send-notification')
async def send_notification(
    request: Request,
    x_admin_key: str = Header(..., alias="x-admin-key")
):
    if x_admin_key != ADMIN_KEY:
        return JSONResponse(status_code=401, content={'error': 'Unauthorized'})

    try:
        body_data = await request.json()
        title = body_data.get('title')
        body = body_data.get('body')
        topic = body_data.get('topic', 'all_users')
        message_type = body_data.get('messageType', 'text')

        if not title or not body:
            return JSONResponse(status_code=400, content={'error': 'Title and body required'})

        # Verify initialization
        try:
            firebase_admin.get_app()
        except Exception:
            init_firebase()

        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            data={
                'messageType': message_type,
                'recipientType': topic,
                'timestamp': str(int(time.time() * 1000))
            },
            topic=topic
        )

        print(f'🚀 Sending to Topic: {topic}')
        response = messaging.send(message)
        return {'success': True, 'messageId': response}

    except Exception as error:
        print('❌ FCM Send Error:', str(error))
        return JSONResponse(status_code=500, content={'error': 'Notification Failed', 'detail': str(error)})

# Send to specific device token - Matches fcm-v1-server.js
@app.post('/api/send-notification-device')
async def send_notification_device(
    request: Request,
    x_admin_key: str = Header(..., alias="x-admin-key")
):
    if x_admin_key != ADMIN_KEY:
        return JSONResponse(status_code=401, content={'error': 'Unauthorized'})

    try:
        body_data = await request.json()
        title = body_data.get('title')
        body = body_data.get('body')
        token = body_data.get('token')
        recipient_type = body_data.get('recipientType', 'parent')
        message_type = body_data.get('messageType', 'text')

        if not title or not body or not token:
            return JSONResponse(status_code=400, content={'error': 'Title, body, and token required'})

        print(f'📱 Sending to Device: {token[:20]}...')

        message = messaging.Message(
            token=token,
            notification=messaging.Notification(title=title, body=body),
            data={
                'type': 'admin_notification',
                'messageType': message_type,
                'recipientType': recipient_type,
                'timestamp': str(int(time.time() * 1000)),
                'source': 'admin_panel',
                'message': body
            },
            android=messaging.AndroidConfig(priority='high')
        )

        response = messaging.send(message)
        return {
            'success': True, 
            'messageId': response,
            'message': 'Notification sent to mobile device'
        }

    except Exception as error:
        print('❌ Device Send Error:', str(error))
        return JSONResponse(status_code=500, content={'detail': f'Failed to send notification: {str(error)}'})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=PORT)
