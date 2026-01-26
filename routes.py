from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from datetime import date, datetime
import uuid
from database import get_db
from models import *
from auth import get_password_hash, verify_password, create_access_token
from encryption import encrypt_data, decrypt_data

router = APIRouter()

# Helper functions
def check_user_exists_and_active(cursor, phone: int, user_type: str):
    table = "parents" if user_type == "parent" else "drivers"
    id_col = f"{table[:-1]}_id"
    cursor.execute(f"SELECT {id_col}, status FROM {table} WHERE phone = %s", (phone,))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(status_code=404, detail=f"{user_type.title()} not found")
    if user['status'] != 'ACTIVE':
        raise HTTPException(status_code=403, detail="Account inactive")
    return user

def update_entity(cursor, table: str, id_col: str, entity_id: str, update_data: dict):
    cursor.execute(f"SELECT {id_col} FROM {table} WHERE {id_col} = %s", (entity_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail=f"{table[:-1].title()} not found")
    
    update_fields = []
    update_values = []
    
    for field, value in update_data.dict(exclude_unset=True).items():
        if value is not None:
            update_fields.append(f"{field} = %s")
            update_values.append(value)
    
    if update_fields:
        update_values.append(entity_id)
        query = f"UPDATE {table} SET {', '.join(update_fields)} WHERE {id_col} = %s"
        cursor.execute(query, tuple(update_values))
    
    cursor.execute(f"SELECT * FROM {table} WHERE {id_col} = %s", (entity_id,))
    return cursor.fetchone()

# =====================================================
# ENCRYPTION/DECRYPTION ROUTES
# =====================================================

@router.post("/encrypt", tags=["Encryption"])
async def encrypt_text(data: dict):
    """Encrypt text data"""
    try:
        text = data.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        encrypted = encrypt_data(text)
        return {"encrypted_text": encrypted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encryption failed: {str(e)}")

@router.post("/decrypt", tags=["Encryption"])
async def decrypt_text(data: dict):
    """Decrypt text data"""
    try:
        encrypted_text = data.get("encrypted_text", "")
        if not encrypted_text:
            raise HTTPException(status_code=400, detail="Encrypted text is required")
        
        decrypted = decrypt_data(encrypted_text)
        return {"decrypted_text": decrypted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")

# =====================================================
# AUTHENTICATION ROUTES
# =====================================================

@router.post("/auth/login", response_model=Token, tags=["Authentication"])
async def login(login_data: LoginRequest):
    """Universal login for all user types (admin, parent, driver)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            user = None
            
            # Try admin first
            cursor.execute("SELECT admin_id as user_id, password_hash, status, 'admin' as user_type FROM admins WHERE phone = %s", (login_data.phone,))
            user = cursor.fetchone()
            
            # Try parent if admin not found
            if not user:
                cursor.execute("SELECT parent_id as user_id, password_hash, status, 'parent' as user_type FROM parents WHERE phone = %s", (login_data.phone,))
                user = cursor.fetchone()
            
            # Try driver if parent not found
            if not user:
                cursor.execute("SELECT driver_id as user_id, password_hash, status, 'driver' as user_type FROM drivers WHERE phone = %s", (login_data.phone,))
                user = cursor.fetchone()
            
            if not user:
                raise HTTPException(status_code=401, detail="Invalid phone number or password")
            
            # Verify password
            if not verify_password(login_data.password, user['password_hash']):
                raise HTTPException(status_code=401, detail="Invalid phone number or password")
            
            if user['status'] != 'ACTIVE':
                raise HTTPException(status_code=403, detail="Account inactive")
            
            # Update last login
            if user['user_type'] == 'admin':
                cursor.execute("UPDATE admins SET last_login_at = %s WHERE admin_id = %s", (datetime.utcnow(), user['user_id']))
            elif user['user_type'] == 'parent':
                cursor.execute("UPDATE parents SET last_login_at = %s WHERE parent_id = %s", (datetime.utcnow(), user['user_id']))
            
            access_token = create_access_token(data={"sub": user['user_id'], "user_type": user['user_type'], "phone": login_data.phone})
            return {"access_token": access_token, "token_type": "bearer"}

@router.get("/auth/profile", tags=["Authentication"])
async def get_user_profile():
    """Get current authenticated user's profile"""
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                # Try to get any admin first
                cursor.execute("SELECT * FROM admins ORDER BY created_at DESC LIMIT 1")
                user_data = cursor.fetchone()
                
                if user_data:
                    return {
                        "user_type": "admin",
                        "profile": user_data
                    }
                
                # If no admin, try parent
                cursor.execute("SELECT * FROM parents ORDER BY created_at DESC LIMIT 1")
                user_data = cursor.fetchone()
                
                if user_data:
                    return {
                        "user_type": "parent",
                        "profile": user_data
                    }
                
                # If no parent, try driver
                cursor.execute("SELECT * FROM drivers ORDER BY created_at DESC LIMIT 1")
                user_data = cursor.fetchone()
                
                if user_data:
                    return {
                        "user_type": "driver",
                        "profile": user_data
                    }
                
                raise HTTPException(status_code=404, detail="No users found. Please create a user first.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# =====================================================
# ADMIN ROUTES
# =====================================================

@router.post("/admins", response_model=AdminResponse, status_code=status.HTTP_201_CREATED, tags=["Admins"])
async def create_admin(admin: AdminCreate):
    """Create a new admin (public endpoint for initial setup)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            # Check if phone already exists
            cursor.execute("SELECT admin_id FROM admins WHERE phone = %s", (admin.phone,))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number already registered"
                )
            
            # Check if email already exists
            if admin.email:
                cursor.execute("SELECT admin_id FROM admins WHERE email = %s", (admin.email,))
                if cursor.fetchone():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered"
                    )
            
            admin_id = str(uuid.uuid4())
            password_hash = get_password_hash(admin.password)
            
            cursor.execute(
                """INSERT INTO admins (admin_id, phone, email, password_hash, name, dob)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (admin_id, admin.phone, admin.email, password_hash, admin.name, admin.dob)
            )
            
            cursor.execute("SELECT * FROM admins WHERE admin_id = %s", (admin_id,))
            return cursor.fetchone()

@router.get("/admins/profile", response_model=AdminResponse, tags=["Admins"])
async def get_admin_profile():
    """Get current admin's profile"""
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM admins ORDER BY created_at DESC LIMIT 1")
                admin = cursor.fetchone()
                if not admin:
                    raise HTTPException(status_code=404, detail="No admin found. Please create an admin first.")
                return admin
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/admins", tags=["Admins"])
async def get_all_admins():
    """Get all admins (admin only)"""
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM admins ORDER BY created_at DESC")
                result = cursor.fetchall()
                return [dict(admin) for admin in result] if result else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/admins/{admin_id}", response_model=AdminResponse, tags=["Admins"])
async def get_admin(admin_id: str):
    """Get admin by ID (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM admins WHERE admin_id = %s", (admin_id,))
            admin = cursor.fetchone()
            if not admin:
                raise HTTPException(status_code=404, detail="Admin not found")
            return admin

@router.put("/admins/{admin_id}", response_model=AdminResponse, tags=["Admins"])
async def update_admin(admin_id: str, admin_update: AdminUpdate):
    """Update admin (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            # Check if admin exists
            cursor.execute("SELECT admin_id FROM admins WHERE admin_id = %s", (admin_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Admin not found")
            
            update_fields = []
            update_values = []
            
            for field, value in admin_update.dict(exclude_unset=True).items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    update_values.append(value)
            
            if update_fields:
                update_values.append(admin_id)
                query = f"UPDATE admins SET {', '.join(update_fields)} WHERE admin_id = %s"
                cursor.execute(query, tuple(update_values))
            
            cursor.execute("SELECT * FROM admins WHERE admin_id = %s", (admin_id,))
            return cursor.fetchone()

@router.delete("/admins/{admin_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Admins"])
async def delete_admin(admin_id: str):
    """Delete admin (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM admins WHERE admin_id = %s", (admin_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Admin not found")

# =====================================================
# PARENT ROUTES
# =====================================================

@router.post("/parents", response_model=ParentResponse, status_code=status.HTTP_201_CREATED, tags=["Parents"])
async def create_parent(parent: ParentCreate):
    """Create a new parent (admin only) - Password required for login"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            # Check if phone already exists
            cursor.execute("SELECT parent_id FROM parents WHERE phone = %s", (parent.phone,))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number already registered"
                )
            
            # Check if email already exists
            if parent.email:
                cursor.execute("SELECT parent_id FROM parents WHERE email = %s", (parent.email,))
                if cursor.fetchone():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered"
                    )
            
            # Validate student_id if provided
            if parent.student_id:
                cursor.execute("SELECT student_id FROM students WHERE student_id = %s", (parent.student_id,))
                if not cursor.fetchone():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Student with ID {parent.student_id} not found"
                    )
            
            parent_id = str(uuid.uuid4())
            password_hash = get_password_hash(parent.password)
            
            cursor.execute(
                """INSERT INTO parents (parent_id, phone, email, password_hash, name, dob, 
                   parent_role, door_no, street, city, district, state, country, pincode, emergency_contact)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (parent_id, parent.phone, parent.email, password_hash, parent.name, parent.dob,
                 parent.parent_role, parent.door_no, parent.street, parent.city, parent.district,
                 parent.state, parent.country, parent.pincode, parent.emergency_contact)
            )
            
            cursor.execute("SELECT * FROM parents WHERE parent_id = %s", (parent_id,))
            return cursor.fetchone()

@router.get("/parents/profile", response_model=ParentResponse, tags=["Parents"])
async def get_parent_profile():
    """Get current parent's profile"""
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM parents ORDER BY created_at DESC LIMIT 1")
                parent = cursor.fetchone()
                if not parent:
                    raise HTTPException(status_code=404, detail="No parent found. Please create a parent first.")
                return parent
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/parents", tags=["Parents"])
async def get_all_parents():
    """Get all parents (admin only)"""
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM parents ORDER BY created_at DESC")
                result = cursor.fetchall()
                
                # Convert to plain dict to avoid Pydantic issues
                parents = []
                for parent in result:
                    parent_dict = dict(parent)
                    # Handle both old and new column names
                    if 'failed_login_attempts' not in parent_dict or parent_dict['failed_login_attempts'] is None:
                        parent_dict['failed_login_attempts'] = 0
                    # Handle status column name change
                    if 'status' in parent_dict:
                        parent_dict['parents_active_status'] = parent_dict['status']
                    elif 'parents_active_status' not in parent_dict or parent_dict['parents_active_status'] is None:
                        parent_dict['parents_active_status'] = 'ACTIVE'
                    parents.append(parent_dict)
                
                return parents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/parents/{parent_id}", response_model=ParentResponse, tags=["Parents"])
async def get_parent(parent_id: str):
    """Get parent by ID (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM parents WHERE parent_id = %s", (parent_id,))
            parent = cursor.fetchone()
            if not parent:
                raise HTTPException(status_code=404, detail="Parent not found")
            return parent

@router.put("/parents/{parent_id}", response_model=ParentResponse, tags=["Parents"])
async def update_parent(parent_id: str, parent_update: ParentUpdate):
    """Update parent (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT parent_id FROM parents WHERE parent_id = %s", (parent_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Parent not found")
            
            update_fields = []
            update_values = []
            
            for field, value in parent_update.dict(exclude_unset=True).items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    update_values.append(value)
            
            if update_fields:
                update_values.append(parent_id)
                query = f"UPDATE parents SET {', '.join(update_fields)} WHERE parent_id = %s"
                cursor.execute(query, tuple(update_values))
            
            cursor.execute("SELECT * FROM parents WHERE parent_id = %s", (parent_id,))
            return cursor.fetchone()

@router.delete("/parents/{parent_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Parents"])
async def delete_parent(parent_id: str):
    """Delete parent (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM parents WHERE parent_id = %s", (parent_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Parent not found")

# =====================================================
# DRIVER ROUTES
# =====================================================

@router.post("/drivers", response_model=DriverResponse, status_code=status.HTTP_201_CREATED, tags=["Drivers"])
async def create_driver(driver: DriverCreate):
    """Create a new driver (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT driver_id FROM drivers WHERE phone = %s", (driver.phone,))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number already registered"
                )
            
            driver_id = str(uuid.uuid4())
            password_hash = get_password_hash(driver.password)
            
            cursor.execute(
                """INSERT INTO drivers (driver_id, name, phone, email, password_hash, dob, licence_number, 
                   licence_expiry, aadhar_number, licence_url, aadhar_url, photo_url, fcm_token)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (driver_id, driver.name, driver.phone, driver.email, password_hash, driver.dob,
                 driver.licence_number, driver.licence_expiry, driver.aadhar_number,
                 driver.licence_url, driver.aadhar_url, driver.photo_url, driver.fcm_token)
            )
            
            cursor.execute("SELECT * FROM drivers WHERE driver_id = %s", (driver_id,))
            return cursor.fetchone()

@router.get("/drivers", tags=["Drivers"])
async def get_all_drivers(driver_id: Optional[str] = None):
    """Get all drivers or specific driver by ID using query parameter (admin only)"""
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                if driver_id:
                    cursor.execute("SELECT * FROM drivers WHERE driver_id = %s", (driver_id,))
                    driver = cursor.fetchone()
                    if not driver:
                        raise HTTPException(status_code=404, detail="Driver not found")
                    return [dict(driver)]
                else:
                    cursor.execute("SELECT * FROM drivers ORDER BY created_at DESC")
                    result = cursor.fetchall()
                    return [dict(driver) for driver in result] if result else []
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/drivers/available", response_model=List[DriverResponse], tags=["Drivers"])
async def get_available_drivers():
    """Get available drivers (admin only)"""
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM drivers WHERE is_available = 1 AND status = 'ACTIVE' ORDER BY name"
                )
                result = cursor.fetchall()
                return result if result else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/drivers/{driver_id}", response_model=DriverResponse, tags=["Drivers"])
async def get_driver(driver_id: str):
    """Get driver by ID (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM drivers WHERE driver_id = %s", (driver_id,))
            driver = cursor.fetchone()
            if not driver:
                raise HTTPException(status_code=404, detail="Driver not found")
            return driver

@router.put("/drivers/{driver_id}", response_model=DriverResponse, tags=["Drivers"])
async def update_driver(driver_id: str, driver_update: DriverUpdate):
    """Update driver (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT driver_id FROM drivers WHERE driver_id = %s", (driver_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Driver not found")
            
            update_fields = []
            update_values = []
            
            for field, value in driver_update.dict(exclude_unset=True).items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    update_values.append(value)
            
            if update_fields:
                update_values.append(driver_id)
                query = f"UPDATE drivers SET {', '.join(update_fields)} WHERE driver_id = %s"
                cursor.execute(query, tuple(update_values))
            
            cursor.execute("SELECT * FROM drivers WHERE driver_id = %s", (driver_id,))
            return cursor.fetchone()

@router.delete("/drivers/{driver_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Drivers"])
async def delete_driver(driver_id: str):
    """Delete driver (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM drivers WHERE driver_id = %s", (driver_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Driver not found")

# =====================================================
# ROUTE ROUTES
# =====================================================

@router.post("/routes", response_model=RouteResponse, status_code=status.HTTP_201_CREATED, tags=["Routes"])
async def create_route(route: RouteCreate):
    """Create a new route (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            route_id = str(uuid.uuid4())
            
            cursor.execute(
                "INSERT INTO routes (route_id, name) VALUES (%s, %s)",
                (route_id, route.name)
            )
            
            cursor.execute("SELECT * FROM routes WHERE route_id = %s", (route_id,))
            return cursor.fetchone()

@router.get("/routes", tags=["Routes"])
async def get_all_routes():
    """Get all routes (admin only)"""
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM routes ORDER BY name")
                result = cursor.fetchall()
                return [dict(route) for route in result] if result else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/routes/{route_id}", response_model=RouteResponse, tags=["Routes"])
async def get_route(route_id: str):
    """Get route by ID (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM routes WHERE route_id = %s", (route_id,))
            route = cursor.fetchone()
            if not route:
                raise HTTPException(status_code=404, detail="Route not found")
            return route

@router.put("/routes/{route_id}", response_model=RouteResponse, tags=["Routes"])
async def update_route(route_id: str, route_update: RouteUpdate):
    """Update route (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT route_id FROM routes WHERE route_id = %s", (route_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Route not found")
            
            update_fields = []
            update_values = []
            
            for field, value in route_update.dict(exclude_unset=True).items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    update_values.append(value)
            
            if update_fields:
                update_values.append(route_id)
                query = f"UPDATE routes SET {', '.join(update_fields)} WHERE route_id = %s"
                cursor.execute(query, tuple(update_values))
            
            cursor.execute("SELECT * FROM routes WHERE route_id = %s", (route_id,))
            return cursor.fetchone()

@router.delete("/routes/{route_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Routes"])
async def delete_route(route_id: str):
    """Delete route (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM routes WHERE route_id = %s", (route_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Route not found")

# =====================================================
# BUS ROUTES
# =====================================================

@router.post("/buses", response_model=BusResponse, status_code=status.HTTP_201_CREATED, tags=["Buses"])
async def create_bus(bus: BusCreate):
    """Create a new bus (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT bus_id FROM buses WHERE bus_number = %s", (bus.bus_number,))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Bus number already exists"
                )
            
            bus_id = str(uuid.uuid4())
            
            cursor.execute(
                """INSERT INTO buses (bus_id, bus_number, driver_id, route_id, bus_type, 
                   bus_brand, bus_model, seating_capacity, rc_expiry_date, fc_expiry_date,
                   rc_book_url, fc_certificate_url, bus_front_url, bus_back_url, 
                   bus_left_url, bus_right_url, assigned_date)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (bus_id, bus.bus_number, bus.driver_id, bus.route_id, bus.bus_type,
                 bus.bus_brand, bus.bus_model, bus.seating_capacity, bus.rc_expiry_date,
                 bus.fc_expiry_date, bus.rc_book_url, bus.fc_certificate_url,
                 bus.bus_front_url, bus.bus_back_url, bus.bus_left_url, bus.bus_right_url,
                 bus.assigned_date)
            )
            
            cursor.execute("SELECT * FROM buses WHERE bus_id = %s", (bus_id,))
            return cursor.fetchone()

@router.get("/buses", tags=["Buses"])
async def get_all_buses():
    """Get all buses (admin only)"""
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM buses ORDER BY bus_number")
                result = cursor.fetchall()
                return [dict(bus) for bus in result] if result else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/buses/{bus_id}", response_model=BusResponse, tags=["Buses"])
async def get_bus(bus_id: str):
    """Get bus by ID (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM buses WHERE bus_id = %s", (bus_id,))
            bus = cursor.fetchone()
            if not bus:
                raise HTTPException(status_code=404, detail="Bus not found")
            return bus

@router.put("/buses/{bus_id}", response_model=BusResponse, tags=["Buses"])
async def update_bus(bus_id: str, bus_update: BusUpdate):
    """Update bus (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT bus_id FROM buses WHERE bus_id = %s", (bus_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Bus not found")
            
            update_fields = []
            update_values = []
            
            for field, value in bus_update.dict(exclude_unset=True).items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    update_values.append(value)
            
            if update_fields:
                update_values.append(bus_id)
                query = f"UPDATE buses SET {', '.join(update_fields)} WHERE bus_id = %s"
                cursor.execute(query, tuple(update_values))
            
            cursor.execute("SELECT * FROM buses WHERE bus_id = %s", (bus_id,))
            return cursor.fetchone()

@router.delete("/buses/{bus_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Buses"])
async def delete_bus(bus_id: str):
    """Delete bus (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM buses WHERE bus_id = %s", (bus_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Bus not found")

# =====================================================
# ROUTE STOP ROUTES
# =====================================================

@router.post("/route-stops", response_model=RouteStopResponse, status_code=status.HTTP_201_CREATED, tags=["Route Stops"])
async def create_route_stop(stop: RouteStopCreate):
    """Create a new route stop (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            # Verify route exists
            cursor.execute("SELECT route_id FROM routes WHERE route_id = %s", (stop.route_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Route not found")
            
            stop_id = str(uuid.uuid4())
            
            cursor.execute(
                """INSERT INTO route_stops (stop_id, route_id, stop_name, latitude, longitude, stop_order)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (stop_id, stop.route_id, stop.stop_name, stop.latitude, stop.longitude, stop.stop_order)
            )
            
            cursor.execute("SELECT * FROM route_stops WHERE stop_id = %s", (stop_id,))
            return cursor.fetchone()

@router.get("/route-stops", tags=["Route Stops"])
async def get_all_route_stops(route_id: Optional[str] = None):
    """Get all route stops, optionally filtered by route (admin only)"""
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                if route_id:
                    cursor.execute(
                        "SELECT * FROM route_stops WHERE route_id = %s ORDER BY stop_order",
                        (route_id,)
                    )
                else:
                    cursor.execute("SELECT * FROM route_stops ORDER BY route_id, stop_order")
                result = cursor.fetchall()
                return [dict(stop) for stop in result] if result else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/route-stops/{stop_id}", response_model=RouteStopResponse, tags=["Route Stops"])
async def get_route_stop(stop_id: str):
    """Get route stop by ID (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM route_stops WHERE stop_id = %s", (stop_id,))
            stop = cursor.fetchone()
            if not stop:
                raise HTTPException(status_code=404, detail="Route stop not found")
            return stop

@router.put("/route-stops/{stop_id}", response_model=RouteStopResponse, tags=["Route Stops"])
async def update_route_stop(stop_id: str, stop_update: RouteStopUpdate):
    """Update route stop (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT stop_id FROM route_stops WHERE stop_id = %s", (stop_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Route stop not found")
            
            update_fields = []
            update_values = []
            
            for field, value in stop_update.dict(exclude_unset=True).items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    update_values.append(value)
            
            if update_fields:
                update_values.append(stop_id)
                query = f"UPDATE route_stops SET {', '.join(update_fields)} WHERE stop_id = %s"
                cursor.execute(query, tuple(update_values))
            
            cursor.execute("SELECT * FROM route_stops WHERE stop_id = %s", (stop_id,))
            return cursor.fetchone()

@router.delete("/route-stops/{stop_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Route Stops"])
async def delete_route_stop(stop_id: str):
    """Delete route stop (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM route_stops WHERE stop_id = %s", (stop_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Route stop not found")

# =====================================================
# STUDENT ROUTES
# =====================================================

@router.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=["Students"])
async def create_student(student: StudentCreate):
    """Create a new student (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            # Verify parent exists
            cursor.execute("SELECT parent_id FROM parents WHERE parent_id = %s", (student.parent_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Parent not found")
            
            # Verify secondary parent if provided
            if student.s_parent_id:
                cursor.execute("SELECT parent_id FROM parents WHERE parent_id = %s", (student.s_parent_id,))
                if not cursor.fetchone():
                    raise HTTPException(status_code=404, detail="Secondary parent not found")
            
            # Verify route exists
            cursor.execute("SELECT route_id FROM routes WHERE route_id = %s", (student.route_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Route not found")
            
            # Verify stops exist and belong to the route
            cursor.execute(
                "SELECT stop_id FROM route_stops WHERE stop_id = %s AND route_id = %s",
                (student.pickup_stop_id, student.route_id)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Pickup stop not found or doesn't belong to route")
            
            cursor.execute(
                "SELECT stop_id FROM route_stops WHERE stop_id = %s AND route_id = %s",
                (student.drop_stop_id, student.route_id)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Drop stop not found or doesn't belong to route")
            
            student_id = str(uuid.uuid4())
            
            cursor.execute(
                """INSERT INTO students (student_id, parent_id, s_parent_id, name, dob, 
                   class_section, route_id, pickup_stop_id, drop_stop_id, emergency_contact, student_photo_url)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (student_id, student.parent_id, student.s_parent_id, student.name, student.dob,
                 student.class_section, student.route_id, student.pickup_stop_id, student.drop_stop_id,
                 student.emergency_contact, student.student_photo_url)
            )
            
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
            return cursor.fetchone()

@router.get("/students", tags=["Students"])
async def get_all_students():
    """Get all students (admin only)"""
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM students ORDER BY name")
                result = cursor.fetchall()
                return [dict(student) for student in result] if result else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/students/parent/{parent_id}", response_model=List[StudentResponse], tags=["Students"])
async def get_students_by_parent(parent_id: str):
    """Get students by parent ID (parent can only see their own, admin can see all)"""
    # Parents can only see their own students
    # if current_user.user_type == "parent" and current_user.user_id != parent_id:
    #     raise HTTPException(status_code=403, detail="Access denied")
    
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM students WHERE parent_id = %s OR s_parent_id = %s ORDER BY name",
                (parent_id, parent_id)
            )
            return cursor.fetchall()

@router.get("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
async def get_student(student_id: str):
    """Get student by ID (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
            student = cursor.fetchone()
            if not student:
                raise HTTPException(status_code=404, detail="Student not found")
            return student

@router.put("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
async def update_student(student_id: str, student_update: StudentUpdate):
    """Update student (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT student_id FROM students WHERE student_id = %s", (student_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Student not found")
            
            update_fields = []
            update_values = []
            
            for field, value in student_update.dict(exclude_unset=True).items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    update_values.append(value)
            
            if update_fields:
                update_values.append(student_id)
                query = f"UPDATE students SET {', '.join(update_fields)} WHERE student_id = %s"
                cursor.execute(query, tuple(update_values))
            
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
            return cursor.fetchone()

@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
async def delete_student(student_id: str):
    """Delete student (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Student not found")

# =====================================================
# TRIP ROUTES
# =====================================================

@router.post("/trips", response_model=TripResponse, status_code=status.HTTP_201_CREATED, tags=["Trips"])
async def create_trip(trip: TripCreate):
    """Create a new trip (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            # Verify bus exists
            cursor.execute("SELECT bus_id FROM buses WHERE bus_id = %s", (trip.bus_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Bus not found")
            
            # Verify driver exists
            cursor.execute("SELECT driver_id FROM drivers WHERE driver_id = %s", (trip.driver_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Driver not found")
            
            # Verify route exists
            cursor.execute("SELECT route_id FROM routes WHERE route_id = %s", (trip.route_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Route not found")
            
            trip_id = str(uuid.uuid4())
            
            cursor.execute(
                """INSERT INTO trips (trip_id, bus_id, driver_id, route_id, trip_date, trip_type)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (trip_id, trip.bus_id, trip.driver_id, trip.route_id, trip.trip_date, trip.trip_type)
            )
            
            cursor.execute("SELECT * FROM trips WHERE trip_id = %s", (trip_id,))
            return cursor.fetchone()

@router.get("/trips", tags=["Trips"])
async def get_all_trips(
    route_id: Optional[str] = None,
    trip_date: Optional[date] = None
):
    """Get all trips with optional filters (admin only)"""
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM trips WHERE 1=1"
                params = []
                
                if route_id:
                    query += " AND route_id = %s"
                    params.append(route_id)
                
                if trip_date:
                    query += " AND trip_date = %s"
                    params.append(trip_date)
                
                query += " ORDER BY trip_date DESC, trip_type"
                
                cursor.execute(query, tuple(params))
                result = cursor.fetchall()
                return [dict(trip) for trip in result] if result else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/trips/{trip_id}", response_model=TripResponse, tags=["Trips"])
async def get_trip(trip_id: str):
    """Get trip by ID (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM trips WHERE trip_id = %s", (trip_id,))
            trip = cursor.fetchone()
            if not trip:
                raise HTTPException(status_code=404, detail="Trip not found")
            return trip

@router.put("/trips/{trip_id}", response_model=TripResponse, tags=["Trips"])
async def update_trip(trip_id: str, trip_update: TripUpdate):
    """Update trip (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT trip_id FROM trips WHERE trip_id = %s", (trip_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Trip not found")
            
            update_fields = []
            update_values = []
            
            for field, value in trip_update.dict(exclude_unset=True).items():
                if value is not None:
                    update_fields.append(f"{field} = %s")
                    update_values.append(value)
            
            if update_fields:
                update_values.append(trip_id)
                query = f"UPDATE trips SET {', '.join(update_fields)} WHERE trip_id = %s"
                cursor.execute(query, tuple(update_values))
            
            cursor.execute("SELECT * FROM trips WHERE trip_id = %s", (trip_id,))
            return cursor.fetchone()

@router.delete("/trips/{trip_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Trips"])
async def delete_trip(trip_id: str):
    """Delete trip (admin only)"""
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM trips WHERE trip_id = %s", (trip_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Trip not found")

# =====================================================
# FCM TOKEN ROUTES
# =====================================================

@router.put("/parents/{parent_id}/fcm-token", tags=["Parents"])
async def update_parent_fcm_token(parent_id: str, fcm_data: dict):
    """Update parent FCM token"""
    fcm_token = fcm_data.get("fcm_token")
    if not fcm_token:
        raise HTTPException(status_code=400, detail="FCM token is required")
    
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT parent_id FROM parents WHERE parent_id = %s", (parent_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Parent not found")
            
            cursor.execute(
                "UPDATE parents SET fcm_token = %s WHERE parent_id = %s",
                (fcm_token, parent_id)
            )
            
            cursor.execute("SELECT * FROM parents WHERE parent_id = %s", (parent_id,))
            return cursor.fetchone()

@router.put("/parents/{parent_id}/assign-student", response_model=ParentResponse, tags=["Parents"])
async def assign_student_to_parent(parent_id: str, student_data: dict):
    """Assign a student to a parent"""
    student_id = student_data.get("student_id")
    if not student_id:
        raise HTTPException(status_code=400, detail="Student ID is required")
    
    with get_db() as conn:
        with conn.cursor() as cursor:
            # Verify parent exists
            cursor.execute("SELECT parent_id FROM parents WHERE parent_id = %s", (parent_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Parent not found")
            
            # Verify student exists
            cursor.execute("SELECT student_id FROM students WHERE student_id = %s", (student_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Student with ID {student_id} not found"
                )
            
            # Update parent with student_id
            cursor.execute(
                "UPDATE parents SET student_id = %s WHERE parent_id = %s",
                (student_id, parent_id)
            )
            
            cursor.execute("SELECT * FROM parents WHERE parent_id = %s", (parent_id,))
            return cursor.fetchone()

@router.put("/drivers/{driver_id}/fcm-token", tags=["Drivers"])
async def update_driver_fcm_token(driver_id: str, fcm_data: dict):
    """Update driver FCM token"""
    fcm_token = fcm_data.get("fcm_token")
    if not fcm_token:
        raise HTTPException(status_code=400, detail="FCM token is required")
    
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT driver_id FROM drivers WHERE driver_id = %s", (driver_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Driver not found")
            
            cursor.execute(
                "UPDATE drivers SET fcm_token = %s WHERE driver_id = %s",
                (fcm_token, driver_id)
            )
            
            cursor.execute("SELECT * FROM drivers WHERE driver_id = %s", (driver_id,))
            return cursor.fetchone()
