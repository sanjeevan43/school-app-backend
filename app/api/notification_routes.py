from fastapi import APIRouter, Header, HTTPException, Body
from app.notification_api.service import notification_service, ADMIN_KEY
from typing import Optional

router = APIRouter()

@router.get("/notifications/status", tags=["Notifications"])
async def get_status():
    """Check notification service status"""
    return {
        "status": "online" if notification_service.initialized else "offline",
        "initialized": notification_service.initialized,
        "creds_found": notification_service.creds_path is not None
    }

@router.post("/notifications/send", tags=["Notifications"])
async def send_notification(
    title: str = Body(...),
    body: str = Body(...),
    topic: str = Body("all_users"),
    message_type: str = Body("text"),
    x_admin_key: str = Header(..., alias="x-admin-key")
):
    """Send a notification to a specific topic"""
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await notification_service.send_to_topic(title, body, topic, message_type)
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error"))
    
    return result

@router.post("/notifications/send-device", tags=["Notifications"])
async def send_device_notification(
    title: str = Body(...),
    body: str = Body(...),
    token: str = Body(...),
    recipient_type: str = Body("parent"),
    message_type: str = Body("text"),
    x_admin_key: str = Header(..., alias="x-admin-key")
):
    """Send a notification to a specific device token"""
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await notification_service.send_to_device(title, body, token, recipient_type, message_type)
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error"))
    
    return result
