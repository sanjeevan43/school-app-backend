import os
import json
import time
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, messaging
import logging

logger = logging.getLogger(__name__)

# Configuration
ADMIN_KEY = 'selvagam-admin-key-2024'

class FCMService:
    def __init__(self):
        self.creds_path = self._resolve_creds_path()
        self.initialized = False
        if self.creds_path:
            self.init_firebase()

    def _resolve_creds_path(self):
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent
        possible_paths = [
            project_root / 'firebase-credentials.json',
            current_dir / 'firebase-credentials.json',
            Path(os.getcwd()) / 'firebase-credentials.json'
        ]
        return next((p for p in possible_paths if p.exists()), None)

    def init_firebase(self):
        try:
            if not self.creds_path:
                return False, "firebase-credentials.json NOT FOUND"

            with open(self.creds_path, 'r', encoding='utf-8') as f:
                service_account = json.load(f)
            
            project_id = service_account.get('project_id')
            if project_id:
                os.environ['GOOGLE_CLOUD_PROJECT'] = project_id
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(self.creds_path)

            try:
                firebase_apps = firebase_admin._apps
                if firebase_apps:
                    for app_name in list(firebase_apps.keys()):
                        firebase_admin.delete_app(firebase_admin.get_app(app_name))
            except Exception as e:
                logger.warning(f"Error during app cleanup: {e}")

            cred = credentials.Certificate(service_account)
            firebase_admin.initialize_app(cred, {
                'projectId': project_id
            })

            logger.info(f"Firebase Admin initialized for: {firebase_admin.get_app().project_id}")
            self.initialized = True
            return True, "Success"
        except Exception as error:
            err_msg = str(error)
            logger.error(f"Firebase Error during init: {err_msg}")
            return False, err_msg

    async def send_to_topic(self, title: str, body: str, topic: str = 'all_users', message_type: str = 'audio', notification_type: str = None):
        try:
            if not self.initialized:
                success, error = self.init_firebase()
                if not success:
                    return {"success": False, "error": f"Firebase not initialized: {error}"}

            # Use notification_type if provided, otherwise use message_type
            final_type = notification_type or message_type or 'admin_notification'

            message = messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                data={
                    'type': final_type,
                    'title': title,
                    'body': body,
                    'messageType': message_type,
                    'recipientType': topic,
                    'timestamp': str(int(time.time() * 1000)),
                    'source': 'admin_panel',
                    'message': body
                },

                android=messaging.AndroidConfig(
                    priority='high',
                    ttl=3600
                ),
                topic=topic
            )

            response = messaging.send(message)
            return {"success": True, "messageId": response}
        except Exception as error:
            logger.error(f"FCM Topic Send Error: {error}")
            return {"success": False, "error": str(error)}

    async def send_to_device(self, title: str, body: str, token: str, recipient_type: str = 'parent', message_type: str = 'audio', notification_type: str = None):
        try:
            if not self.initialized:
                success, error = self.init_firebase()
                if not success:
                    return {"success": False, "error": f"Firebase not initialized: {error}"}

            # Use notification_type if provided, otherwise use message_type
            final_type = notification_type or message_type or 'admin_notification'

            message = messaging.Message(
                token=token,
                notification=messaging.Notification(title=title, body=body),
                data={
                    'type': final_type,
                    'title': title,
                    'body': body,
                    'messageType': message_type,
                    'recipientType': recipient_type,
                    'timestamp': str(int(time.time() * 1000)),
                    'source': 'admin_panel',
                    'message': body
                },

                android=messaging.AndroidConfig(priority='high')
            )

            response = messaging.send(message)
            return {"success": True, "messageId": response}
        except Exception as error:
            logger.error(f"FCM Device Send Error: {error}")
            return {"success": False, "error": str(error)}

    async def send_force_logout(self, token: str):
        try:
            if not self.initialized:
                success, error = self.init_firebase()
                if not success:
                    return {"success": False, "error": f"Firebase not initialized: {error}"}

            message = messaging.Message(
                token=token,
                notification=messaging.Notification(
                    title="Session Expired",
                    body="You have been logged in on another device"
                ),
                data={
                    "type": "FORCE_LOGOUT",
                    "messageType": "text",
                    "source": "system"
                },
                android=messaging.AndroidConfig(priority='high')
            )

            response = messaging.send(message)
            return {"success": True, "messageId": response}
        except Exception as error:
            logger.error(f"FCM Force Logout Error: {error}")
            return {"success": False, "error": str(error)}


# Global instance
notification_service = FCMService()
