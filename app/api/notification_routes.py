from fastapi import APIRouter, Header, HTTPException, Body, status
from app.notification_api.service import notification_service, ADMIN_KEY
from typing import Optional, List
from app.api.models import *
from app.core.database import execute_query
from app.core.auth import create_access_token
from datetime import datetime

router = APIRouter()

@router.post("/auth/login", response_model=Token, tags=["Authentication"])
async def login(login_data: LoginRequest):
    """Universal login for all user types (admin, parent, driver)"""
    try:
        # Check admins table
        admin_query = "SELECT admin_id, phone, password_hash, name FROM admins WHERE phone = %s AND status = 'ACTIVE'"
        admin = execute_query(admin_query, (login_data.phone,), fetch_one=True)
        
        if admin and admin['password_hash'] == login_data.password:
            # Update last login
            execute_query("UPDATE admins SET last_login_at = %s WHERE admin_id = %s", 
                         (datetime.now(), admin['admin_id']))
            
            access_token = create_access_token(
                data={"sub": admin['admin_id'], "user_type": "admin", "phone": admin['phone']}
            )
            return {"access_token": access_token, "token_type": "bearer"}
        
        # Check parents table
        parent_query = "SELECT parent_id, phone, password_hash, name FROM parents WHERE phone = %s AND parents_active_status = 'ACTIVE'"
        parent = execute_query(parent_query, (login_data.phone,), fetch_one=True)
        
        if parent and parent['password_hash'] == login_data.password:
            # Update last login
            execute_query("UPDATE parents SET last_login_at = %s WHERE parent_id = %s", 
                         (datetime.now(), parent['parent_id']))
            
            access_token = create_access_token(
                data={"sub": parent['parent_id'], "user_type": "parent", "phone": parent['phone']}
            )
            return {"access_token": access_token, "token_type": "bearer"}
        
        # Check drivers table
        driver_query = "SELECT driver_id, phone, password_hash, name FROM drivers WHERE phone = %s AND status = 'ACTIVE'"
        driver = execute_query(driver_query, (login_data.phone,), fetch_one=True)
        
        if driver and driver['password_hash'] == login_data.password:
            access_token = create_access_token(
                data={"sub": driver['driver_id'], "user_type": "driver", "phone": driver['phone']}
            )
            return {"access_token": access_token, "token_type": "bearer"}
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password"
        )
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

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
    
    # Fetch all driver tokens
    drivers = execute_query("SELECT fcm_token FROM drivers WHERE fcm_token IS NOT NULL AND status = 'ACTIVE'", fetch_all=True)
    
    results = []
    for d in drivers:
        if d['fcm_token']:
            res = await notification_service.send_to_device(title, body, d['fcm_token'], recipient_type="driver")
            results.append(res)
            
    return {"success": True, "delivered_count": len(results), "total_found": len(drivers)}

@router.post("/notifications/broadcast/parents", tags=["Notifications"])
async def broadcast_parents(
    title: str = Body(..., description="The title of the notification"),
    body: str = Body(..., description="The message body"),
    x_admin_key: str = Header(..., alias="x-admin-key")
):
    """Send a notification to all parents"""
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Fetch all unique parent tokens from database
    tokens = execute_query("SELECT DISTINCT fcm_token FROM fcm_tokens WHERE parent_id IS NOT NULL", fetch_all=True)
    
    # Extract tokens
    all_tokens = [t['fcm_token'] for t in tokens if t['fcm_token']]
    
    results = []
    for t_val in all_tokens:
        # Defaulting to parent/text for this specific broadcast
        res = await notification_service.send_to_device(title, body, t_val, recipient_type="parent", message_type="text")
        results.append(res)
        
    return {"success": True, "delivered_count": len(results), "total_found": len(tokens), "message": f"Broadcast sent to {len(results)} devices"}

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
