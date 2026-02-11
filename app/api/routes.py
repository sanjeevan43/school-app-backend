from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime, date
import uuid
import logging
import json

from app.core.database import get_db, execute_query
from app.api.models import *
from app.core.auth import create_access_token
from app.core.encryption import encrypt_data, decrypt_data
from app.services.bus_tracking import bus_tracking_service, fcm_service
from app.services.cascade_updates import cascade_service

router = APIRouter()
logger = logging.getLogger(__name__)

# =====================================================
# AUTHENTICATION ENDPOINTS
# =====================================================

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
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@router.get("/auth/profile", tags=["Authentication"])
async def get_profile(phone: int):
    """Get user profile by phone number"""
    try:
        # Check admins table
        admin_query = "SELECT admin_id, phone, email, name, status, last_login_at, created_at FROM admins WHERE phone = %s"
        admin = execute_query(admin_query, (phone,), fetch_one=True)
        
        if admin:
            return {
                "user_type": "admin",
                "user_id": admin['admin_id'],
                "phone": admin['phone'],
                "email": admin['email'],
                "name": admin['name'],
                "status": admin['status'],
                "last_login_at": admin['last_login_at'],
                "created_at": admin['created_at']
            }
        
        # Check parents table
        parent_query = "SELECT parent_id, phone, email, name, parent_role, parents_active_status, last_login_at, created_at FROM parents WHERE phone = %s"
        parent = execute_query(parent_query, (phone,), fetch_one=True)
        
        if parent:
            return {
                "user_type": "parent",
                "user_id": parent['parent_id'],
                "phone": parent['phone'],
                "email": parent['email'],
                "name": parent['name'],
                "parent_role": parent['parent_role'],
                "status": parent['parents_active_status'],
                "last_login_at": parent['last_login_at'],
                "created_at": parent['created_at']
            }
        
        # Check drivers table
        driver_query = "SELECT driver_id, phone, email, name, licence_number, status, created_at FROM drivers WHERE phone = %s"
        driver = execute_query(driver_query, (phone,), fetch_one=True)
        
        if driver:
            return {
                "user_type": "driver",
                "user_id": driver['driver_id'],
                "phone": driver['phone'],
                "email": driver['email'],
                "name": driver['name'],
                "licence_number": driver['licence_number'],
                "status": driver['status'],
                "created_at": driver['created_at']
            }
        
        raise HTTPException(status_code=404, detail="User not found")
        
    except Exception as e:
        logger.error(f"Get profile error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get profile")

# =====================================================
# ADMIN ENDPOINTS
# =====================================================

@router.post("/admins", response_model=AdminResponse, tags=["Admins"])
async def create_admin(admin: AdminCreate):
    """Create a new admin"""
    try:
        admin_id = str(uuid.uuid4())
        query = """
        INSERT INTO admins (admin_id, phone, email, password_hash, name)
        VALUES (%s, %s, %s, %s, %s)
        """
        execute_query(query, (admin_id, admin.phone, admin.email, admin.password, admin.name))
        
        return await get_admin(admin_id)
    except Exception as e:
        logger.error(f"Create admin error: {e}")
        raise HTTPException(status_code=400, detail="Failed to create admin")

@router.get("/admins", response_model=List[AdminResponse], tags=["Admins"])
async def get_all_admins():
    """Get all admins"""
    query = "SELECT * FROM admins ORDER BY created_at DESC"
    admins = execute_query(query, fetch_all=True)
    return admins or []

@router.get("/admins/{admin_id}", response_model=AdminResponse, tags=["Admins"])
async def get_admin(admin_id: str):
    """Get admin by ID"""
    query = "SELECT * FROM admins WHERE admin_id = %s"
    admin = execute_query(query, (admin_id,), fetch_one=True)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

@router.put("/admins/{admin_id}", response_model=AdminResponse, tags=["Admins"])
async def update_admin(admin_id: str, admin_update: AdminUpdate):
    """Update admin"""
    update_fields = []
    values = []
    
    for field, value in admin_update.dict(exclude_unset=True).items():
        if value is not None:
            update_fields.append(f"{field} = %s")
            values.append(value)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    values.append(admin_id)
    query = f"UPDATE admins SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE admin_id = %s"
    
    result = execute_query(query, tuple(values))
    if result == 0:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    return await get_admin(admin_id)

@router.put("/admins/{admin_id}/status", response_model=AdminResponse, tags=["Admins"])
async def update_admin_status(admin_id: str, status_update: StatusUpdate):
    """Update admin status only"""
    query = "UPDATE admins SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE admin_id = %s"
    result = execute_query(query, (status_update.status.value, admin_id))
    if result == 0:
        raise HTTPException(status_code=404, detail="Admin not found")
    return await get_admin(admin_id)

@router.delete("/admins/{admin_id}", tags=["Admins"])
async def delete_admin(admin_id: str):
    """Delete admin"""
    query = "DELETE FROM admins WHERE admin_id = %s"
    result = execute_query(query, (admin_id,))
    if result == 0:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"message": "Admin deleted successfully"}

# =====================================================
# PARENT ENDPOINTS
# =====================================================

@router.post("/parents", response_model=ParentResponse, tags=["Parents"])
async def create_parent(parent: ParentCreate):
    """Create a new parent"""
    try:
        parent_id = str(uuid.uuid4())
        query = """
        INSERT INTO parents (parent_id, phone, email, password_hash, name, parent_role, 
                           door_no, street, city, district, pincode)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        result = execute_query(query, (parent_id, parent.phone, parent.email, parent.password, 
                             parent.name, parent.parent_role.value, parent.door_no, parent.street,
                             parent.city, parent.district, parent.pincode))
        
        if result == 0:
            raise HTTPException(status_code=400, detail="Failed to insert parent")
        
        return await get_parent(parent_id)
    except Exception as e:
        logger.error(f"Create parent error: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to create parent: {str(e)}")

@router.get("/parents", response_model=List[ParentResponse], tags=["Parents"])
async def get_all_parents():
    """Get all parents"""
    query = "SELECT * FROM parents ORDER BY created_at DESC"
    parents = execute_query(query, fetch_all=True)
    return parents or []

@router.get("/parents/{parent_id}", response_model=ParentResponse, tags=["Parents"])
async def get_parent(parent_id: str):
    """Get parent by ID"""
    query = "SELECT * FROM parents WHERE parent_id = %s"
    parent = execute_query(query, (parent_id,), fetch_one=True)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent

@router.put("/parents/{parent_id}", response_model=ParentResponse, tags=["Parents"])
async def update_parent(parent_id: str, parent_update: ParentUpdate):
    """Update parent with cascade updates"""
    try:
        # Get old data for cascade comparison
        old_parent = execute_query("SELECT * FROM parents WHERE parent_id = %s", (parent_id,), fetch_one=True)
        if not old_parent:
            raise HTTPException(status_code=404, detail="Parent not found")
        
        update_fields = []
        values = []
        
        for field, value in parent_update.dict(exclude_unset=True).items():
            if value is not None:
                update_fields.append(f"{field} = %s")
                values.append(value)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(parent_id)
        query = f"UPDATE parents SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE parent_id = %s"
        
        result = execute_query(query, tuple(values))
        if result == 0:
            raise HTTPException(status_code=404, detail="Parent not found")
        
        # Trigger cascade updates
        new_data = parent_update.dict(exclude_unset=True)
        cascade_service.update_parent_cascades(parent_id, old_parent, new_data)
        
        return await get_parent(parent_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update parent error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update parent")

@router.put("/parents/{parent_id}/status", response_model=ParentResponse, tags=["Parents"])
async def update_parent_status(parent_id: str, status_update: StatusUpdate):
    """Update parent status only"""
    query = "UPDATE parents SET parents_active_status = %s, updated_at = CURRENT_TIMESTAMP WHERE parent_id = %s"
    result = execute_query(query, (status_update.status.value, parent_id))
    if result == 0:
        raise HTTPException(status_code=404, detail="Parent not found")
    return await get_parent(parent_id)

@router.put("/parents/{parent_id}/fcm-token", tags=["Parents"])
async def update_parent_fcm_token(parent_id: str, fcm_data: dict):
    """Update FCM token for parent when they login"""
    try:
        fcm_token = fcm_data.get("fcm_token")
        if not fcm_token:
            raise HTTPException(status_code=400, detail="fcm_token is required")
        
        # Check if parent exists
        parent = execute_query("SELECT parent_id FROM parents WHERE parent_id = %s", (parent_id,), fetch_one=True)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent not found")
        
        # Update or insert FCM token
        query = """
        INSERT INTO fcm_tokens (fcm_id, fcm_token, parent_id) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        fcm_token = VALUES(fcm_token),
        updated_at = CURRENT_TIMESTAMP
        """
        fcm_id = str(uuid.uuid4())
        execute_query(query, (fcm_id, fcm_token, parent_id))
        
        return {
            "message": "FCM token updated successfully",
            "parent_id": parent_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update parent FCM token error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update FCM token")

@router.patch("/parents/{parent_id}/fcm-token", tags=["Parents"])
async def patch_parent_fcm_token(parent_id: str, fcm_data: dict):
    """PATCH: Update parent FCM token"""
    try:
        fcm_token = fcm_data.get("fcm_token")
        if not fcm_token:
            raise HTTPException(status_code=400, detail="fcm_token is required")
        
        # Check if parent exists
        parent = execute_query("SELECT parent_id FROM parents WHERE parent_id = %s", (parent_id,), fetch_one=True)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent not found")
        
        # Update or insert FCM token
        query = """
        INSERT INTO fcm_tokens (fcm_id, fcm_token, parent_id) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        fcm_token = VALUES(fcm_token),
        updated_at = CURRENT_TIMESTAMP
        """
        fcm_id = str(uuid.uuid4())
        execute_query(query, (fcm_id, fcm_token, parent_id))
        
        return {
            "message": "FCM token updated successfully",
            "parent_id": parent_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update parent FCM token error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update FCM token")

@router.get("/parents/fcm-tokens/all", tags=["Parents"])
async def get_all_parent_fcm_tokens():
    """GET: Retrieve all parent FCM tokens"""
    query = """
    SELECT p.parent_id, p.name, p.phone, f.fcm_token, p.parents_active_status 
    FROM parents p
    INNER JOIN fcm_tokens f ON p.parent_id = f.parent_id
    WHERE p.parents_active_status = 'ACTIVE' AND f.fcm_token IS NOT NULL
    ORDER BY p.name
    """
    parents = execute_query(query, fetch_all=True)
    return {"parents": parents or [], "count": len(parents) if parents else 0}

@router.delete("/parents/{parent_id}", tags=["Parents"])
async def delete_parent(parent_id: str):
    """Delete parent with cascade cleanup"""
    try:
        # Get parent data for cascade cleanup
        parent_data = execute_query("SELECT * FROM parents WHERE parent_id = %s", (parent_id,), fetch_one=True)
        if not parent_data:
            raise HTTPException(status_code=404, detail="Parent not found")
        
        # Perform cascade cleanup
        cascade_service.delete_cascades("parents", parent_id, parent_data)
        
        # Delete parent
        query = "DELETE FROM parents WHERE parent_id = %s"
        result = execute_query(query, (parent_id,))
        if result == 0:
            raise HTTPException(status_code=404, detail="Parent not found")
        
        return {"message": "Parent deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete parent error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete parent")

# =====================================================
# DRIVER ENDPOINTS
# =====================================================

@router.post("/drivers", response_model=DriverResponse, tags=["Drivers"])
async def create_driver(driver: DriverCreate):
    """Create a new driver"""
    try:
        driver_id = str(uuid.uuid4())
        query = """
        INSERT INTO drivers (driver_id, name, phone, email, licence_number, licence_expiry, 
                           password_hash, fcm_token)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (driver_id, driver.name, driver.phone, driver.email,
                             driver.licence_number, driver.licence_expiry, driver.password,
                             driver.fcm_token))
        
        return await get_driver(driver_id)
    except Exception as e:
        logger.error(f"Create driver error: {e}")
        raise HTTPException(status_code=400, detail="Failed to create driver")

@router.get("/drivers", response_model=List[DriverResponse], tags=["Drivers"])
async def get_all_drivers(status: Optional[DriverStatus] = None):
    """Get all drivers, optionally filtered by status"""
    if status:
        query = "SELECT * FROM drivers WHERE status = %s ORDER BY created_at DESC"
        drivers = execute_query(query, (status.value,), fetch_all=True)
    else:
        query = "SELECT * FROM drivers ORDER BY created_at DESC"
        drivers = execute_query(query, fetch_all=True)
    return drivers or []

@router.get("/drivers/{driver_id}", response_model=DriverResponse, tags=["Drivers"])
async def get_driver(driver_id: str):
    """Get driver by ID"""
    query = "SELECT * FROM drivers WHERE driver_id = %s"
    driver = execute_query(query, (driver_id,), fetch_one=True)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@router.put("/drivers/{driver_id}", response_model=DriverResponse, tags=["Drivers"])
async def update_driver(driver_id: str, driver_update: DriverUpdate):
    """Update driver"""
    update_fields = []
    values = []
    
    for field, value in driver_update.dict(exclude_unset=True).items():
        if value is not None:
            update_fields.append(f"{field} = %s")
            values.append(value)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    values.append(driver_id)
    query = f"UPDATE drivers SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE driver_id = %s"
    
    result = execute_query(query, tuple(values))
    if result == 0:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    return await get_driver(driver_id)

@router.put("/drivers/{driver_id}/status", response_model=DriverResponse, tags=["Drivers"])
async def update_driver_status(driver_id: str, status_update: DriverStatusUpdate):
    """Update driver status only (ACTIVE, INACTIVE, SUSPENDED)"""
    query = "UPDATE drivers SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE driver_id = %s"
    result = execute_query(query, (status_update.status.value, driver_id))
    if result == 0:
        raise HTTPException(status_code=404, detail="Driver not found")
    return await get_driver(driver_id)

@router.patch("/drivers/{driver_id}/fcm-token", response_model=DriverResponse, tags=["Drivers"])
async def patch_driver_fcm_token(driver_id: str, fcm_data: dict):
    """PATCH: Update driver FCM token"""
    fcm_token = fcm_data.get("fcm_token")
    if not fcm_token:
        raise HTTPException(status_code=400, detail="fcm_token is required")
    
    query = "UPDATE drivers SET fcm_token = %s, updated_at = CURRENT_TIMESTAMP WHERE driver_id = %s"
    result = execute_query(query, (fcm_token, driver_id))
    if result == 0:
        raise HTTPException(status_code=404, detail="Driver not found")
    return await get_driver(driver_id)

@router.get("/drivers/fcm-tokens/all", tags=["Drivers"])
async def get_all_driver_fcm_tokens():
    """GET: Retrieve all driver FCM tokens"""
    query = """
    SELECT driver_id, name, phone, fcm_token, status 
    FROM drivers 
    WHERE fcm_token IS NOT NULL AND fcm_token != '' AND status = 'ACTIVE'
    ORDER BY name
    """
    drivers = execute_query(query, fetch_all=True)
    return {"drivers": drivers or [], "count": len(drivers) if drivers else 0}

@router.delete("/drivers/{driver_id}", tags=["Drivers"])
async def delete_driver(driver_id: str):
    """Delete driver"""
    query = "DELETE FROM drivers WHERE driver_id = %s"
    result = execute_query(query, (driver_id,))
    if result == 0:
        raise HTTPException(status_code=404, detail="Driver not found")
    return {"message": "Driver deleted successfully"}

# =====================================================
# ROUTE ENDPOINTS
# =====================================================

@router.post("/routes", response_model=RouteResponse, tags=["Routes"])
async def create_route(route: RouteCreate):
    """Create a new route"""
    try:
        route_id = str(uuid.uuid4())
        query = "INSERT INTO routes (route_id, name) VALUES (%s, %s)"
        execute_query(query, (route_id, route.name))
        
        return await get_route(route_id)
    except Exception as e:
        logger.error(f"Create route error: {e}")
        raise HTTPException(status_code=400, detail="Failed to create route")

@router.get("/routes", response_model=List[RouteResponse], tags=["Routes"])
async def get_all_routes():
    """Get all routes"""
    query = "SELECT * FROM routes ORDER BY created_at DESC"
    routes = execute_query(query, fetch_all=True)
    return routes or []

@router.get("/routes/{route_id}", response_model=RouteResponse, tags=["Routes"])
async def get_route(route_id: str):
    """Get route by ID"""
    query = "SELECT * FROM routes WHERE route_id = %s"
    route = execute_query(query, (route_id,), fetch_one=True)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.put("/routes/{route_id}", response_model=RouteResponse, tags=["Routes"])
async def update_route(route_id: str, route_update: RouteUpdate):
    """Update route with cascade updates"""
    try:
        # Get old data for cascade comparison
        old_route = execute_query("SELECT * FROM routes WHERE route_id = %s", (route_id,), fetch_one=True)
        if not old_route:
            raise HTTPException(status_code=404, detail="Route not found")
        
        update_fields = []
        values = []
        
        for field, value in route_update.dict(exclude_unset=True).items():
            if value is not None:
                update_fields.append(f"{field} = %s")
                values.append(value)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(route_id)
        query = f"UPDATE routes SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE route_id = %s"
        
        result = execute_query(query, tuple(values))
        if result == 0:
            raise HTTPException(status_code=404, detail="Route not found")
        
        # Trigger cascade updates
        new_data = route_update.dict(exclude_unset=True)
        cascade_service.update_route_cascades(route_id, old_route, new_data)
        
        return await get_route(route_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update route error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update route")

@router.put("/routes/{route_id}/status", response_model=RouteResponse, tags=["Routes"])
async def update_route_status(route_id: str, status_update: StatusUpdate):
    """Update route status only"""
    query = "UPDATE routes SET routes_active_status = %s, updated_at = CURRENT_TIMESTAMP WHERE route_id = %s"
    result = execute_query(query, (status_update.status.value, route_id))
    if result == 0:
        raise HTTPException(status_code=404, detail="Route not found")
    return await get_route(route_id)

@router.delete("/routes/{route_id}", tags=["Routes"])
async def delete_route(route_id: str):
    """Delete route with cascade cleanup"""
    try:
        # Get route data for cascade cleanup
        route_data = execute_query("SELECT * FROM routes WHERE route_id = %s", (route_id,), fetch_one=True)
        if not route_data:
            raise HTTPException(status_code=404, detail="Route not found")
        
        # Perform cascade cleanup
        cascade_service.delete_cascades("routes", route_id, route_data)
        
        # Delete route
        query = "DELETE FROM routes WHERE route_id = %s"
        result = execute_query(query, (route_id,))
        if result == 0:
            raise HTTPException(status_code=404, detail="Route not found")
        
        return {"message": "Route deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete route error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete route")

# =====================================================
# ROUTE STOP ENDPOINTS
# =====================================================

@router.post("/route-stops", response_model=RouteStopResponse, tags=["Route Stops"])
async def create_route_stop(route_stop: RouteStopCreate):
    """Create a new route stop"""
    try:
        stop_id = str(uuid.uuid4())
        query = """
        INSERT INTO route_stops (stop_id, route_id, stop_name, latitude, longitude, 
                               pickup_stop_order, drop_stop_order)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (stop_id, route_stop.route_id, route_stop.stop_name,
                             route_stop.latitude, route_stop.longitude, 
                             route_stop.pickup_stop_order, route_stop.drop_stop_order))
        
        return await get_route_stop(stop_id)
    except Exception as e:
        logger.error(f"Create route stop error: {e}")
        raise HTTPException(status_code=400, detail="Failed to create route stop")

@router.get("/route-stops", response_model=List[RouteStopResponse], tags=["Route Stops"])
async def get_all_route_stops(route_id: Optional[str] = None):
    """Get all route stops, optionally filtered by route"""
    if route_id:
        query = "SELECT * FROM route_stops WHERE route_id = %s ORDER BY pickup_stop_order"
        stops = execute_query(query, (route_id,), fetch_all=True)
    else:
        query = "SELECT * FROM route_stops ORDER BY route_id, pickup_stop_order"
        stops = execute_query(query, fetch_all=True)
    return stops or []

@router.get("/route-stops/{stop_id}", response_model=RouteStopResponse, tags=["Route Stops"])
async def get_route_stop(stop_id: str):
    """Get route stop by ID"""
    query = "SELECT * FROM route_stops WHERE stop_id = %s"
    stop = execute_query(query, (stop_id,), fetch_one=True)
    if not stop:
        raise HTTPException(status_code=404, detail="Route stop not found")
    return stop

@router.put("/route-stops/{stop_id}", response_model=RouteStopResponse, tags=["Route Stops"])
async def update_route_stop(stop_id: str, stop_update: RouteStopUpdate):
    """Update route stop with cascade updates"""
    try:
        # Get old data for cascade comparison
        old_stop = execute_query("SELECT * FROM route_stops WHERE stop_id = %s", (stop_id,), fetch_one=True)
        if not old_stop:
            raise HTTPException(status_code=404, detail="Route stop not found")
        
        update_fields = []
        values = []
        
        for field, value in stop_update.dict(exclude_unset=True).items():
            if value is not None:
                update_fields.append(f"{field} = %s")
                values.append(value)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(stop_id)
        query = f"UPDATE route_stops SET {', '.join(update_fields)} WHERE stop_id = %s"
        
        result = execute_query(query, tuple(values))
        if result == 0:
            raise HTTPException(status_code=404, detail="Route stop not found")
        
        # Trigger cascade updates
        new_data = stop_update.dict(exclude_unset=True)
        cascade_service.update_route_stop_cascades(stop_id, old_stop, new_data)
        
        return await get_route_stop(stop_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update route stop error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update route stop")

@router.delete("/route-stops/{stop_id}", tags=["Route Stops"])
async def delete_route_stop(stop_id: str):
    """Delete route stop with cascade cleanup"""
    try:
        # Get stop data for cascade cleanup
        stop_data = execute_query("SELECT * FROM route_stops WHERE stop_id = %s", (stop_id,), fetch_one=True)
        if not stop_data:
            raise HTTPException(status_code=404, detail="Route stop not found")
        
        # Perform cascade cleanup
        cascade_service.delete_cascades("route_stops", stop_id, stop_data)
        
        # Delete route stop
        query = "DELETE FROM route_stops WHERE stop_id = %s"
        result = execute_query(query, (stop_id,))
        if result == 0:
            raise HTTPException(status_code=404, detail="Route stop not found")
        
        return {"message": "Route stop deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete route stop error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete route stop")

# =====================================================
# BUS ENDPOINTS
# =====================================================

@router.post("/buses", response_model=BusResponse, tags=["Buses"])
async def create_bus(bus: BusCreate):
    """Create a new bus"""
    try:
        bus_id = str(uuid.uuid4())
        query = """
        INSERT INTO buses (bus_id, registration_number, driver_id, route_id, vehicle_type,
                          bus_brand, bus_model, seating_capacity, rc_expiry_date, fc_expiry_date,
                          rc_book_url, fc_certificate_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (bus_id, bus.registration_number, bus.driver_id, bus.route_id,
                             bus.vehicle_type, bus.bus_brand, bus.bus_model, bus.seating_capacity,
                             bus.rc_expiry_date, bus.fc_expiry_date, bus.rc_book_url, 
                             bus.fc_certificate_url))
        
        return await get_bus(bus_id)
    except Exception as e:
        logger.error(f"Create bus error: {e}")
        raise HTTPException(status_code=400, detail="Failed to create bus")

@router.get("/buses", response_model=List[BusResponse], tags=["Buses"])
async def get_all_buses(status: Optional[BusStatus] = None):
    """Get all buses, optionally filtered by status"""
    if status:
        query = "SELECT * FROM buses WHERE status = %s ORDER BY created_at DESC"
        buses = execute_query(query, (status.value,), fetch_all=True)
    else:
        query = "SELECT * FROM buses ORDER BY created_at DESC"
        buses = execute_query(query, fetch_all=True)
    return buses or []

@router.get("/buses/{bus_id}", response_model=BusResponse, tags=["Buses"])
async def get_bus(bus_id: str):
    """Get bus by ID"""
    query = "SELECT * FROM buses WHERE bus_id = %s"
    bus = execute_query(query, (bus_id,), fetch_one=True)
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    return bus

@router.put("/buses/{bus_id}", response_model=BusResponse, tags=["Buses"])
async def update_bus(bus_id: str, bus_update: BusUpdate):
    """Update bus"""
    update_fields = []
    values = []
    
    for field, value in bus_update.dict(exclude_unset=True).items():
        if value is not None:
            update_fields.append(f"{field} = %s")
            values.append(value)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    values.append(bus_id)
    query = f"UPDATE buses SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE bus_id = %s"
    
    result = execute_query(query, tuple(values))
    if result == 0:
        raise HTTPException(status_code=404, detail="Bus not found")
    
    return await get_bus(bus_id)

@router.put("/buses/{bus_id}/status", response_model=BusResponse, tags=["Buses"])
async def update_bus_status(bus_id: str, status_update: BusStatusUpdate):
    """Update bus status only (ACTIVE, INACTIVE, MAINTENANCE, SCRAP, SPARE)"""
    query = "UPDATE buses SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE bus_id = %s"
    result = execute_query(query, (status_update.status.value, bus_id))
    if result == 0:
        raise HTTPException(status_code=404, detail="Bus not found")
    return await get_bus(bus_id)

@router.patch("/buses/{bus_id}/status", response_model=BusResponse, tags=["Buses"])
async def patch_bus_status(bus_id: str, status_update: BusStatusUpdate):
    """PATCH: Update bus status only (ACTIVE, INACTIVE, MAINTENANCE, SCRAP, SPARE)"""
    query = "UPDATE buses SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE bus_id = %s"
    result = execute_query(query, (status_update.status.value, bus_id))
    if result == 0:
        raise HTTPException(status_code=404, detail="Bus not found")
    return await get_bus(bus_id)

@router.patch("/buses/{bus_id}/driver", response_model=BusResponse, tags=["Buses"])
async def assign_bus_driver(bus_id: str, assignment: BusDriverAssign):
    """PATCH: Assign or reasssign driver to bus. Set driver_id to null to unassign."""
    # Verify bus exists
    bus = execute_query("SELECT bus_id FROM buses WHERE bus_id = %s", (bus_id,), fetch_one=True)
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    # If driver_id is provided, verify driver exists
    if assignment.driver_id:
        driver = execute_query("SELECT driver_id FROM drivers WHERE driver_id = %s", (assignment.driver_id,), fetch_one=True)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
            
    query = "UPDATE buses SET driver_id = %s, updated_at = CURRENT_TIMESTAMP WHERE bus_id = %s"
    logger.info(f"Assigning driver {assignment.driver_id} to bus {bus_id}")
    execute_query(query, (assignment.driver_id, bus_id))
    
    return await get_bus(bus_id)

@router.patch("/buses/{bus_id}/route", response_model=BusResponse, tags=["Buses"])
async def patch_bus_route(bus_id: str, route_data: dict):
    """PATCH: Assign route to bus"""
    route_id = route_data.get("route_id")
    if not route_id:
        raise HTTPException(status_code=400, detail="route_id is required")
    
    query = "UPDATE buses SET route_id = %s, updated_at = CURRENT_TIMESTAMP WHERE bus_id = %s"
    result = execute_query(query, (route_id, bus_id))
    if result == 0:
        raise HTTPException(status_code=404, detail="Bus not found")
    return await get_bus(bus_id)

@router.patch("/buses/{bus_id}/documents", response_model=BusResponse, tags=["Buses"])
async def patch_bus_documents(bus_id: str, documents: dict):
    """PATCH: Update bus document URLs (rc_book_url, fc_certificate_url)"""
    update_fields = []
    values = []
    
    if "rc_book_url" in documents and documents["rc_book_url"]:
        update_fields.append("rc_book_url = %s")
        values.append(documents["rc_book_url"])
    
    if "fc_certificate_url" in documents and documents["fc_certificate_url"]:
        update_fields.append("fc_certificate_url = %s")
        values.append(documents["fc_certificate_url"])
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No document URLs provided")
    
    values.append(bus_id)
    query = f"UPDATE buses SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE bus_id = %s"
    
    result = execute_query(query, tuple(values))
    if result == 0:
        raise HTTPException(status_code=404, detail="Bus not found")
    return await get_bus(bus_id)

@router.get("/buses/driver/{driver_id}", response_model=BusResponse, tags=["Buses"])
async def get_bus_by_driver(driver_id: str):
    """Get bus assigned to a specific driver"""
    query = """
    SELECT bus_id, registration_number, driver_id, route_id, vehicle_type, 
           bus_brand, bus_model, seating_capacity, rc_expiry_date, fc_expiry_date,
           rc_book_url, fc_certificate_url, status, created_at, updated_at
    FROM buses 
    WHERE driver_id = %s
    LIMIT 1
    """
    result = execute_query(query, (driver_id,), fetch_one=True)
    if not result:
        raise HTTPException(status_code=404, detail="No bus found for this driver")
    return result

@router.delete("/buses/{bus_id}", tags=["Buses"])
async def delete_bus(bus_id: str):
    """Delete bus"""
    query = "DELETE FROM buses WHERE bus_id = %s"
    result = execute_query(query, (bus_id,))
    if result == 0:
        raise HTTPException(status_code=404, detail="Bus not found")
    return {"message": "Bus deleted successfully"}

# =====================================================
# CLASS ENDPOINTS
# =====================================================

@router.post("/classes", response_model=ClassResponse, tags=["Classes"])
async def create_class(class_data: ClassCreate):
    """Create a new class"""
    try:
        class_id = str(uuid.uuid4())
        query = """
        INSERT INTO classes (class_id, class_name, section, academic_year)
        VALUES (%s, %s, %s, %s)
        """
        execute_query(query, (class_id, class_data.class_name, class_data.section, 
                             class_data.academic_year))
        
        return await get_class(class_id)
    except Exception as e:
        logger.error(f"Create class error: {e}")
        raise HTTPException(status_code=400, detail="Failed to create class")

@router.get("/classes", response_model=List[ClassResponse], tags=["Classes"])
async def get_all_classes():
    """Get all classes"""
    query = "SELECT * FROM classes ORDER BY class_name, section"
    classes = execute_query(query, fetch_all=True)
    return classes or []

@router.get("/classes/{class_id}", response_model=ClassResponse, tags=["Classes"])
async def get_class(class_id: str):
    """Get class by ID"""
    query = "SELECT * FROM classes WHERE class_id = %s"
    class_data = execute_query(query, (class_id,), fetch_one=True)
    if not class_data:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_data

@router.put("/classes/{class_id}", response_model=ClassResponse, tags=["Classes"])
async def update_class(class_id: str, class_update: ClassUpdate):
    """Update class"""
    update_fields = []
    values = []
    
    for field, value in class_update.dict(exclude_unset=True).items():
        if value is not None:
            update_fields.append(f"{field} = %s")
            values.append(value)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    values.append(class_id)
    query = f"UPDATE classes SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE class_id = %s"
    
    result = execute_query(query, tuple(values))
    if result == 0:
        raise HTTPException(status_code=404, detail="Class not found")
    
    return await get_class(class_id)

@router.put("/classes/{class_id}/status", response_model=ClassResponse, tags=["Classes"])
async def update_class_status(class_id: str, status_update: StatusUpdate):
    """Update class status only"""
    query = "UPDATE classes SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE class_id = %s"
    result = execute_query(query, (status_update.status.value, class_id))
    if result == 0:
        raise HTTPException(status_code=404, detail="Class not found")
    return await get_class(class_id)

@router.delete("/classes/{class_id}", tags=["Classes"])
async def delete_class(class_id: str):
    """Delete class"""
    query = "DELETE FROM classes WHERE class_id = %s"
    result = execute_query(query, (class_id,))
    if result == 0:
        raise HTTPException(status_code=404, detail="Class not found")
    return {"message": "Class deleted successfully"}

# =====================================================
# STUDENT ENDPOINTS
# =====================================================

@router.post("/students", response_model=StudentResponse, tags=["Students"])
async def create_student(student: StudentCreate):
    """Create a new student"""
    try:
        student_id = str(uuid.uuid4())
        query = """
        INSERT INTO students (student_id, parent_id, s_parent_id, name, dob, class_id,
                            pickup_route_id, drop_route_id, pickup_stop_id, drop_stop_id,
                            emergency_contact, student_photo_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (student_id, student.parent_id, student.s_parent_id, student.name,
                             student.dob, student.class_id, student.pickup_route_id, 
                             student.drop_route_id, student.pickup_stop_id, student.drop_stop_id,
                             student.emergency_contact, student.student_photo_url))
        
        return await get_student(student_id)
    except Exception as e:
        logger.error(f"Create student error: {e}")
        # Provide more specific error message
        error_msg = str(e)
        if "foreign key constraint" in error_msg.lower():
            if "parent_id" in error_msg:
                raise HTTPException(status_code=400, detail="Invalid parent_id: Parent not found")
            elif "class_id" in error_msg:
                raise HTTPException(status_code=400, detail="Invalid class_id: Class not found")
            elif "pickup_route_id" in error_msg:
                raise HTTPException(status_code=400, detail="Invalid pickup_route_id: Route not found")
            elif "drop_route_id" in error_msg:
                raise HTTPException(status_code=400, detail="Invalid drop_route_id: Route not found")
            elif "pickup_stop_id" in error_msg:
                raise HTTPException(status_code=400, detail="Invalid pickup_stop_id: Stop not found or doesn't belong to the pickup route")
            elif "drop_stop_id" in error_msg:
                raise HTTPException(status_code=400, detail="Invalid drop_stop_id: Stop not found or doesn't belong to the drop route")
            else:
                raise HTTPException(status_code=400, detail=f"Database constraint error: {error_msg}")
        raise HTTPException(status_code=400, detail=f"Failed to create student: {error_msg}")

@router.get("/students", response_model=List[StudentResponse], tags=["Students"])
async def get_all_students(
    student_status: Optional[StudentStatus] = None,
    transport_status: Optional[TransportStatus] = None
):
    """Get all students with optional filters for student_status and transport_status"""
    conditions = []
    params = []
    
    if student_status:
        conditions.append("student_status = %s")
        params.append(student_status.value)
    
    if transport_status:
        conditions.append("transport_status = %s")
        params.append(transport_status.value)
    
    if conditions:
        query = f"SELECT * FROM students WHERE {' AND '.join(conditions)} ORDER BY created_at DESC"
        students = execute_query(query, tuple(params), fetch_all=True)
    else:
        query = "SELECT * FROM students ORDER BY created_at DESC"
        students = execute_query(query, fetch_all=True)
    
    return students or []

@router.get("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
async def get_student(student_id: str):
    """Get student by ID"""
    query = "SELECT * FROM students WHERE student_id = %s"
    student = execute_query(query, (student_id,), fetch_one=True)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
async def update_student(student_id: str, student_update: StudentUpdate):
    """Update student with cascade updates"""
    try:
        # Get old data for cascade comparison
        old_student = execute_query("SELECT * FROM students WHERE student_id = %s", (student_id,), fetch_one=True)
        if not old_student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        update_fields = []
        values = []
        
        for field, value in student_update.dict(exclude_unset=True).items():
            if value is not None:
                update_fields.append(f"{field} = %s")
                values.append(value)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(student_id)
        query = f"UPDATE students SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE student_id = %s"
        
        result = execute_query(query, tuple(values))
        if result == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Trigger cascade updates
        new_data = student_update.dict(exclude_unset=True)
        cascade_service.update_student_cascades(student_id, old_student, new_data)
        
        return await get_student(student_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update student error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update student")

@router.put("/students/{student_id}/status", response_model=StudentResponse, tags=["Students"])
async def update_student_status(student_id: str, status_update: StudentStatusUpdate):
    """Update student status only (CURRENT, ALUMNI, DISCONTINUED, LONG_ABSENT)"""
    query = "UPDATE students SET student_status = %s, updated_at = CURRENT_TIMESTAMP WHERE student_id = %s"
    result = execute_query(query, (status_update.status.value, student_id))
    if result == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return await get_student(student_id)

@router.patch("/students/{student_id}/status", response_model=StudentResponse, tags=["Students"])
async def patch_student_status(student_id: str, status_update: CombinedStatusUpdate):
    """PATCH: Update student status and/or transport status
    
    - student_status: CURRENT, ALUMNI, DISCONTINUED, LONG_ABSENT
    - transport_status: ACTIVE, TEMP_STOP, CANCELLED
    """
    update_fields = []
    values = []
    
    if status_update.student_status:
        update_fields.append("student_status = %s")
        values.append(status_update.student_status.value)
    
    if status_update.transport_status:
        update_fields.append("transport_status = %s")
        values.append(status_update.transport_status.value)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="At least one status field must be provided")
    
    values.append(student_id)
    query = f"UPDATE students SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE student_id = %s"
    result = execute_query(query, tuple(values))
    
    if result == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return await get_student(student_id)

@router.patch("/students/{student_id}/secondary-parent", response_model=StudentResponse, tags=["Students"])
async def patch_student_secondary_parent(student_id: str, parent_data: SecondaryParentUpdate):
    """PATCH: Assign secondary parent to student. Set to null to unassign."""
    s_parent_id = parent_data.s_parent_id
    
    if s_parent_id:
        # Verify parent exists
        parent_check = execute_query("SELECT parent_id FROM parents WHERE parent_id = %s", (s_parent_id,), fetch_one=True)
        if not parent_check:
            raise HTTPException(status_code=404, detail="Parent not found")
    
    query = "UPDATE students SET s_parent_id = %s, updated_at = CURRENT_TIMESTAMP WHERE student_id = %s"
    result = execute_query(query, (s_parent_id, student_id))
    if result == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return await get_student(student_id)

@router.delete("/students/{student_id}", tags=["Students"])
async def delete_student(student_id: str):
    """Delete student with cascade cleanup"""
    try:
        # Get student data for cascade cleanup
        student_data = execute_query("SELECT * FROM students WHERE student_id = %s", (student_id,), fetch_one=True)
        if not student_data:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Perform cascade cleanup
        cascade_service.delete_cascades("students", student_id, student_data)
        
        # Delete student
        query = "DELETE FROM students WHERE student_id = %s"
        result = execute_query(query, (student_id,))
        if result == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        
        return {"message": "Student deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete student error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete student")

# =====================================================
# TRIP ENDPOINTS
# =====================================================

@router.post("/trips", response_model=TripResponse, tags=["Trips"])
async def create_trip(trip: TripCreate):
    """Create a new trip"""
    try:
        trip_id = str(uuid.uuid4())
        query = """
        INSERT INTO trips (trip_id, bus_id, driver_id, route_id, trip_date, trip_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (trip_id, trip.bus_id, trip.driver_id, trip.route_id,
                             trip.trip_date, trip.trip_type))
        
        return await get_trip(trip_id)
    except Exception as e:
        logger.error(f"Create trip error: {e}")
        raise HTTPException(status_code=400, detail="Failed to create trip")

@router.get("/trips", response_model=List[TripResponse], tags=["Trips"])
async def get_all_trips():
    """Get all trips"""
    query = "SELECT * FROM trips ORDER BY trip_date DESC, created_at DESC"
    trips = execute_query(query, fetch_all=True)
    return trips or []

@router.get("/trips/{trip_id}", response_model=TripResponse, tags=["Trips"])
async def get_trip(trip_id: str):
    """Get trip by ID"""
    query = "SELECT * FROM trips WHERE trip_id = %s"
    trip = execute_query(query, (trip_id,), fetch_one=True)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.put("/trips/{trip_id}", response_model=TripResponse, tags=["Trips"])
async def update_trip(trip_id: str, trip_update: TripUpdate):
    """Update trip"""
    update_fields = []
    values = []
    
    for field, value in trip_update.dict(exclude_unset=True).items():
        update_fields.append(f"{field} = %s")
        values.append(value)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    values.append(trip_id)
    query = f"UPDATE trips SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE trip_id = %s"
    
    result = execute_query(query, tuple(values))
    if result == 0:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    return await get_trip(trip_id)

@router.put("/trips/{trip_id}/status", response_model=TripResponse, tags=["Trips"])
async def update_trip_status(trip_id: str, status_update: TripStatusUpdate):
    """Update trip status only"""
    query = "UPDATE trips SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE trip_id = %s"
    result = execute_query(query, (status_update.status.value, trip_id))
    if result == 0:
        raise HTTPException(status_code=404, detail="Trip not found")
    return await get_trip(trip_id)

@router.delete("/trips/{trip_id}", tags=["Trips"])
async def delete_trip(trip_id: str):
    """Delete trip"""
    query = "DELETE FROM trips WHERE trip_id = %s"
    result = execute_query(query, (trip_id,))
    if result == 0:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"message": "Trip deleted successfully"}

# =====================================================
# ERROR HANDLING ENDPOINTS
# =====================================================

@router.post("/error-handling", response_model=ErrorHandlingResponse, tags=["Error Handling"])
async def create_error_log(error: ErrorHandlingCreate):
    """Create a new error log"""
    try:
        error_id = str(uuid.uuid4())
        query = """
        INSERT INTO error_handling (error_id, error_type, error_code, error_description)
        VALUES (%s, %s, %s, %s)
        """
        execute_query(query, (error_id, error.error_type, error.error_code, error.error_description))
        
        return await get_error_log(error_id)
    except Exception as e:
        logger.error(f"Create error log error: {e}")
        raise HTTPException(status_code=400, detail="Failed to create error log")

@router.get("/error-handling", response_model=List[ErrorHandlingResponse], tags=["Error Handling"])
async def get_all_error_logs():
    """Get all error logs"""
    query = "SELECT * FROM error_handling ORDER BY created_at DESC"
    errors = execute_query(query, fetch_all=True)
    return errors or []

@router.get("/error-handling/{error_id}", response_model=ErrorHandlingResponse, tags=["Error Handling"])
async def get_error_log(error_id: str):
    """Get error log by ID"""
    query = "SELECT * FROM error_handling WHERE error_id = %s"
    error = execute_query(query, (error_id,), fetch_one=True)
    if not error:
        raise HTTPException(status_code=404, detail="Error log not found")
    return error

@router.put("/error-handling/{error_id}", response_model=ErrorHandlingResponse, tags=["Error Handling"])
async def update_error_log(error_id: str, error_update: ErrorHandlingUpdate):
    """Update error log"""
    update_fields = []
    values = []
    
    for field, value in error_update.dict(exclude_unset=True).items():
        if value is not None:
            update_fields.append(f"{field} = %s")
            values.append(value)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    values.append(error_id)
    query = f"UPDATE error_handling SET {', '.join(update_fields)} WHERE error_id = %s"
    
    result = execute_query(query, tuple(values))
    if result == 0:
        raise HTTPException(status_code=404, detail="Error log not found")
    
    return await get_error_log(error_id)

@router.delete("/error-handling/{error_id}", tags=["Error Handling"])
async def delete_error_log(error_id: str):
    """Delete error log"""
    query = "DELETE FROM error_handling WHERE error_id = %s"
    result = execute_query(query, (error_id,))
    if result == 0:
        raise HTTPException(status_code=404, detail="Error log not found")
    return {"message": "Error log deleted successfully"}

# =====================================================
# ENCRYPTION ENDPOINTS
# =====================================================

@router.post("/encrypt", tags=["Encryption"])
async def encrypt_text(data: dict):
    """Encrypt text data"""
    try:
        text = data.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="Text field is required")
        
        encrypted = encrypt_data(text)
        return {"encrypted_text": encrypted}
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        raise HTTPException(status_code=500, detail="Encryption failed")

@router.post("/decrypt", tags=["Encryption"])
async def decrypt_text(data: dict):
    """Decrypt text data"""
    try:
        encrypted_text = data.get("encrypted_text", "")
        if not encrypted_text:
            raise HTTPException(status_code=400, detail="encrypted_text field is required")
        
        decrypted = decrypt_data(encrypted_text)
        return {"decrypted_text": decrypted}
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        raise HTTPException(status_code=500, detail="Decryption failed")

# =====================================================
# UTILITY ENDPOINTS
# =====================================================

@router.get("/students/by-parent/{parent_id}", response_model=List[StudentResponse], tags=["Students"])
async def get_students_by_parent(parent_id: str):
    """Get all students for a specific parent"""
    query = "SELECT * FROM students WHERE parent_id = %s OR s_parent_id = %s ORDER BY name"
    students = execute_query(query, (parent_id, parent_id), fetch_all=True)
    return students or []

@router.get("/trips/by-driver/{driver_id}", response_model=List[TripResponse], tags=["Trips"])
async def get_trips_by_driver(driver_id: str):
    """Get all trips for a specific driver"""
    query = "SELECT * FROM trips WHERE driver_id = %s ORDER BY trip_date DESC"
    trips = execute_query(query, (driver_id,), fetch_all=True)
    return trips or []

@router.get("/trips/by-route/{route_id}", response_model=List[TripResponse], tags=["Trips"])
async def get_trips_by_route(route_id: str):
    """Get all trips for a specific route"""
    query = "SELECT * FROM trips WHERE route_id = %s ORDER BY trip_date DESC"
    trips = execute_query(query, (route_id,), fetch_all=True)
    return trips or []

@router.get("/students/by-route/{route_id}", response_model=List[StudentResponse], tags=["Students"])
async def get_students_by_route(route_id: str):
    """Get all students using a specific route"""
    query = """
    SELECT * FROM students 
    WHERE pickup_route_id = %s OR drop_route_id = %s 
    ORDER BY name
    """
    students = execute_query(query, (route_id, route_id), fetch_all=True)
    return students or []

# =====================================================
# FCM TOKEN ENDPOINTS
# =====================================================

@router.post("/fcm-tokens", response_model=FCMTokenResponse, tags=["FCM Tokens"])
async def create_fcm_token(fcm_token: FCMTokenCreate):
    """Create or update FCM token"""
    try:
        fcm_id = str(uuid.uuid4())
        query = """
        INSERT INTO fcm_tokens (fcm_id, fcm_token, student_id, parent_id)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        student_id = VALUES(student_id),
        parent_id = VALUES(parent_id),
        updated_at = CURRENT_TIMESTAMP
        """
        execute_query(query, (fcm_id, fcm_token.fcm_token, fcm_token.student_id, fcm_token.parent_id))
        
        return await get_fcm_token(fcm_id)
    except Exception as e:
        logger.error(f"Create FCM token error: {e}")
        raise HTTPException(status_code=400, detail="Failed to create FCM token")

@router.get("/fcm-tokens", response_model=List[FCMTokenResponse], tags=["FCM Tokens"])
async def get_all_fcm_tokens():
    """Get all FCM tokens"""
    query = "SELECT * FROM fcm_tokens ORDER BY created_at DESC"
    tokens = execute_query(query, fetch_all=True)
    return tokens or []

@router.get("/fcm-tokens/{fcm_id}", response_model=FCMTokenResponse, tags=["FCM Tokens"])
async def get_fcm_token(fcm_id: str):
    """Get FCM token by ID"""
    query = "SELECT * FROM fcm_tokens WHERE fcm_id = %s"
    token = execute_query(query, (fcm_id,), fetch_one=True)
    if not token:
        raise HTTPException(status_code=404, detail="FCM token not found")
    return token

@router.put("/fcm-tokens/{fcm_id}", response_model=FCMTokenResponse, tags=["FCM Tokens"])
async def update_fcm_token(fcm_id: str, fcm_update: FCMTokenUpdate):
    """Update FCM token with cascade updates"""
    try:
        # Get old data for cascade comparison
        old_token = execute_query("SELECT * FROM fcm_tokens WHERE fcm_id = %s", (fcm_id,), fetch_one=True)
        if not old_token:
            raise HTTPException(status_code=404, detail="FCM token not found")
        
        update_fields = []
        values = []
        
        for field, value in fcm_update.dict(exclude_unset=True).items():
            if value is not None:
                update_fields.append(f"{field} = %s")
                values.append(value)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(fcm_id)
        query = f"UPDATE fcm_tokens SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE fcm_id = %s"
        
        result = execute_query(query, tuple(values))
        if result == 0:
            raise HTTPException(status_code=404, detail="FCM token not found")
        
        # Trigger cascade updates
        new_data = fcm_update.dict(exclude_unset=True)
        cascade_service.update_fcm_token_cascades(fcm_id, old_token, new_data)
        
        return await get_fcm_token(fcm_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update FCM token error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update FCM token")

@router.get("/fcm-tokens/by-route/{route_id}", tags=["FCM Tokens"])
async def get_fcm_tokens_by_route(route_id: str):
    """Get FCM tokens for all stops in a route"""
    try:
        query = """
        SELECT 
            rs.stop_id,
            rs.stop_name,
            rs.pickup_stop_order,
            rs.drop_stop_order,
            s.student_id,
            s.name as student_name,
            ft.fcm_token,
            ft.parent_id,
            p.name as parent_name
        FROM route_stops rs
        LEFT JOIN students s ON (
            (rs.stop_id = s.pickup_stop_id AND s.pickup_route_id = rs.route_id) OR
            (rs.stop_id = s.drop_stop_id AND s.drop_route_id = rs.route_id)
        )
        LEFT JOIN fcm_tokens ft ON (s.student_id = ft.student_id OR s.parent_id = ft.parent_id OR s.s_parent_id = ft.parent_id)
        LEFT JOIN parents p ON ft.parent_id = p.parent_id
        WHERE rs.route_id = %s AND s.transport_status = 'ACTIVE'
        ORDER BY rs.pickup_stop_order, s.name
        """
        
        results = execute_query(query, (route_id,), fetch_all=True)
        
        # Group by stops
        stops_data = {}
        for row in results:
            stop_id = row['stop_id']
            if stop_id not in stops_data:
                stops_data[stop_id] = {
                    "stop_id": stop_id,
                    "stop_name": row['stop_name'],
                    "pickup_stop_order": row['pickup_stop_order'],
                    "drop_stop_order": row['drop_stop_order'],
                    "fcm_tokens": []
                }
            
            if row['fcm_token']:
                # Avoid duplicates if any
                token_entry = {
                    "fcm_token": row['fcm_token'],
                    "parent_id": row['parent_id'],
                    "parent_name": row['parent_name']
                }
                if token_entry not in stops_data[stop_id]["fcm_tokens"]:
                    stops_data[stop_id]["fcm_tokens"].append(token_entry)
        
        return {
            "route_id": route_id,
            "stops": list(stops_data.values()),
            "total_stops": len(stops_data),
            "total_tokens": sum(len(stop["fcm_tokens"]) for stop in stops_data.values())
        }
        
    except Exception as e:
        logger.error(f"Get FCM tokens by route error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get FCM tokens by route")

@router.get("/fcm-tokens/by-stop/{stop_id}", tags=["FCM Tokens"])
async def get_fcm_tokens_by_stop(stop_id: str):
    """Get FCM tokens for one specific stop"""
    try:
        query = """
        SELECT 
            rs.stop_id,
            rs.stop_name,
            rs.pickup_stop_order,
            rs.drop_stop_order,
            s.student_id,
            s.name as student_name,
            ft.fcm_token,
            ft.parent_id,
            p.name as parent_name
        FROM route_stops rs
        LEFT JOIN students s ON (
            (rs.stop_id = s.pickup_stop_id) OR
            (rs.stop_id = s.drop_stop_id)
        )
        LEFT JOIN fcm_tokens ft ON (s.student_id = ft.student_id OR s.parent_id = ft.parent_id OR s.s_parent_id = ft.parent_id)
        LEFT JOIN parents p ON ft.parent_id = p.parent_id
        WHERE rs.stop_id = %s AND s.transport_status = 'ACTIVE'
        ORDER BY s.name
        """
        
        results = execute_query(query, (stop_id,), fetch_all=True)
        
        if not results:
            raise HTTPException(status_code=404, detail="Stop not found")
        
        fcm_tokens = []
        stop_info = None
        
        for row in results:
            if not stop_info:
                stop_info = {
                    "stop_id": row['stop_id'],
                    "stop_name": row['stop_name'],
                    "pickup_stop_order": row['pickup_stop_order'],
                    "drop_stop_order": row['drop_stop_order']
                }
            
            if row['fcm_token']:
                token_entry = {
                    "fcm_token": row['fcm_token'],
                    "parent_id": row['parent_id'],
                    "parent_name": row['parent_name']
                }
                if token_entry not in fcm_tokens:
                    fcm_tokens.append(token_entry)
        
        return {
            "stop_info": stop_info,
            "fcm_tokens": fcm_tokens,
            "total_tokens": len(fcm_tokens)
        }
        
    except Exception as e:
        logger.error(f"Get FCM tokens by stop error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get FCM tokens by stop")

@router.delete("/fcm-tokens/{fcm_id}", tags=["FCM Tokens"])
async def delete_fcm_token(fcm_id: str):
    """Delete FCM token"""
    query = "DELETE FROM fcm_tokens WHERE fcm_id = %s"
    result = execute_query(query, (fcm_id,))
    if result == 0:
        raise HTTPException(status_code=404, detail="FCM token not found")
    return {"message": "FCM token deleted successfully"}

# =====================================================
# BUS TRACKING ENDPOINTS
# =====================================================

@router.post("/bus-tracking/location", tags=["Bus Tracking"])
async def update_bus_location(location_data: BusLocationUpdate):
    """Automatic bus tracking - handles stop progression and trip completion"""
    try:
        result = bus_tracking_service.update_bus_location(
            trip_id=location_data.trip_id,
            latitude=location_data.latitude,
            longitude=location_data.longitude
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result.get("message", "Failed to process location"))
            
    except Exception as e:
        logger.error(f"Bus location processing error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process bus location")

@router.post("/bus-tracking/notify", tags=["Bus Tracking"])
async def send_custom_notification(notification: NotificationRequest):
    """Send custom notification to parents"""
    try:
        # Get trip details
        trip_query = "SELECT * FROM trips WHERE trip_id = %s"
        trip = execute_query(trip_query, (notification.trip_id,), fetch_one=True)
        
        if not trip:
            raise HTTPException(status_code=404, detail="Trip not found")
        
        # Get students for the route
        if notification.stop_id:
            students_query = """
            SELECT s.student_id FROM students s
            WHERE (s.pickup_stop_id = %s OR s.drop_stop_id = %s)
            AND s.transport_status = 'ACTIVE'
            """
            students = execute_query(students_query, (notification.stop_id, notification.stop_id), fetch_all=True)
        else:
            students_query = """
            SELECT s.student_id FROM students s
            WHERE (s.pickup_route_id = %s OR s.drop_route_id = %s)
            AND s.transport_status = 'ACTIVE'
            """
            students = execute_query(students_query, (trip['route_id'], trip['route_id']), fetch_all=True)
        
        if students:
            student_ids = [s['student_id'] for s in students]
            parent_tokens = bus_tracking_service.get_parent_tokens_for_students(student_ids)
            
            if parent_tokens:
                result = fcm_service.send_notification(
                    tokens=parent_tokens,
                    title="Bus Notification",
                    body=notification.message,
                    data={"trip_id": notification.trip_id, "custom": "true"}
                )
                
                return {
                    "success": True,
                    "parents_notified": len(parent_tokens),
                    "students_count": len(students),
                    "notification_result": result
                }
        
        return {"success": False, "message": "No parents to notify"}
        
    except Exception as e:
        logger.error(f"Custom notification error: {e}")
        raise HTTPException(status_code=500, detail="Failed to send notification")

@router.post("/bus-tracking/cache-update/{route_id}", tags=["Bus Tracking"])
async def update_fcm_cache(route_id: str):
    """Update FCM token cache for a route"""
    try:
        result = bus_tracking_service.update_route_fcm_cache(route_id)
        return result
    except Exception as e:
        logger.error(f"FCM cache update error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update FCM cache")

@router.get("/bus-tracking/cache/{route_id}", tags=["Bus Tracking"])
async def get_fcm_cache(route_id: str):
    """Get FCM cache for a route"""
    query = "SELECT * FROM route_stop_fcm_cache WHERE route_id = %s"
    cache = execute_query(query, (route_id,), fetch_one=True)
    
    if not cache:
        raise HTTPException(status_code=404, detail="FCM cache not found for route")
    
    return {
        "route_id": cache['route_id'],
        "stop_fcm_map": json.loads(cache['stop_fcm_map']),
        "updated_at": cache['updated_at']
    }

@router.get("/trips/active", response_model=List[TripResponse], tags=["Trips"])
async def get_active_trips():
    """Get all active/ongoing trips"""
    query = "SELECT * FROM trips WHERE status IN ('ONGOING', 'NOT_STARTED') ORDER BY trip_date DESC"
    trips = execute_query(query, fetch_all=True)
    return trips or []

@router.put("/trips/{trip_id}/start", response_model=TripResponse, tags=["Trips"])
async def start_trip(trip_id: str):
    """Driver starts trip - everything else becomes automatic"""
    try:
        # Update trip status to ONGOING
        query = """
        UPDATE trips SET 
        status = 'ONGOING', 
        started_at = CURRENT_TIMESTAMP,
        current_stop_order = 0,
        updated_at = CURRENT_TIMESTAMP 
        WHERE trip_id = %s AND status = 'NOT_STARTED'
        """
        
        result = execute_query(query, (trip_id,))
        if result == 0:
            raise HTTPException(status_code=404, detail="Trip not found or already started")
        
        return await get_trip(trip_id)
    except Exception as e:
        logger.error(f"Start trip error: {e}")
        raise HTTPException(status_code=500, detail="Failed to start trip")

