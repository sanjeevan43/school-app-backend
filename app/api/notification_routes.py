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

@router.post("/send-notification", tags=["Notifications"])
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

@router.post("/notifications/broadcast/drivers", tags=["Notifications"])
async def broadcast_drivers(
    title: str = Body(...),
    body: str = Body(...),
    x_admin_key: str = Header(..., alias="x-admin-key")
):
    """Send a notification to all drivers"""
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await notification_service.send_to_topic(title, body, topic="drivers")

@router.post("/notifications/broadcast/parents", tags=["Notifications"])
async def broadcast_parents(
    title: str = Body(...),
    body: str = Body(...),
    x_admin_key: str = Header(..., alias="x-admin-key")
):
    """Send a notification to all parents"""
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await notification_service.send_to_topic(title, body, topic="parents")

@router.post("/notifications/student/{student_id}", tags=["Notifications"])
async def send_student_notification(
    student_id: str,
    title: str = Body(...),
    body: str = Body(...),
    x_admin_key: str = Header(..., alias="x-admin-key")
):
    """Send a notification to all FCM tokens associated with a student"""
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    from app.core.database import execute_query
    tokens = execute_query("SELECT fcm_token FROM fcm_tokens WHERE student_id = %s", (student_id,), fetch_all=True)
    if not tokens:
        raise HTTPException(status_code=404, detail="No FCM tokens found for this student")
    
    results = []
    for t in tokens:
        res = await notification_service.send_to_device(title, body, t['fcm_token'], recipient_type="student")
        results.append(res)
    
    return {"success": True, "details": results}

@router.post("/notifications/parent/{parent_id}", tags=["Notifications"])
async def send_parent_notification(
    parent_id: str,
    title: str = Body(...),
    body: str = Body(...),
    x_admin_key: str = Header(..., alias="x-admin-key")
):
    """Send a notification to all FCM tokens associated with a parent"""
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    from app.core.database import execute_query
    tokens = execute_query("SELECT fcm_token FROM fcm_tokens WHERE parent_id = %s", (parent_id,), fetch_all=True)
    if not tokens:
        raise HTTPException(status_code=404, detail="No FCM tokens found for this parent")
    
    results = []
    for t in tokens:
        res = await notification_service.send_to_device(title, body, t['fcm_token'], recipient_type="parent")
        results.append(res)
    
    return {"success": True, "details": results}

@router.post("/notifications/route/{route_id}", tags=["Notifications"])
async def send_route_notification(
    route_id: str,
    title: str = Body(...),
    body: str = Body(...),
    x_admin_key: str = Header(..., alias="x-admin-key")
):
    """Send a notification to everyone (parents/students) on a specific route"""
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    from app.core.database import execute_query
    query = """
    SELECT DISTINCT ft.fcm_token 
    FROM fcm_tokens ft
    JOIN students s ON (ft.student_id = s.student_id OR ft.parent_id = s.parent_id OR ft.parent_id = s.s_parent_id)
    WHERE s.pickup_route_id = %s OR s.drop_route_id = %s
    """
    tokens = execute_query(query, (route_id, route_id), fetch_all=True)
    if not tokens:
        raise HTTPException(status_code=404, detail="No FCM tokens found for this route")
    
    results = []
    for t in tokens:
        res = await notification_service.send_to_device(title, body, t['fcm_token'], recipient_type="route")
        results.append(res)
    
    return {"success": True, "count": len(results)}
