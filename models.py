from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import Optional, Literal
from datetime import date, datetime
from enum import Enum

# Enums
class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class UserType(str, Enum):
    ADMIN = "admin"
    PARENT = "parent"
    DRIVER = "driver"

class ParentRole(str, Enum):
    FATHER = "FATHER"
    MOTHER = "MOTHER"
    GUARDIAN = "GUARDIAN"

class StudentStatus(str, Enum):
    CURRENT = "CURRENT"
    ALUMNI = "ALUMNI"
    DISCONTINUED = "DISCONTINUED"

class TransportStatus(str, Enum):
    ACTIVE = "ACTIVE"
    TEMP_STOP = "TEMP_STOP"
    CANCELLED = "CANCELLED"

class TripType(str, Enum):
    MORNING = "MORNING"
    EVENING = "EVENING"

class TripStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    ONGOING = "ONGOING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"

# Admin Models
class AdminBase(BaseModel):
    phone: int = Field(..., ge=1000000000, le=9999999999)
    email: Optional[EmailStr] = None
    name: str = Field(..., max_length=100)
    dob: Optional[date] = None

class AdminCreate(AdminBase):
    password: str = Field(..., min_length=6, max_length=72)  # Only for initial admin setup

class AdminUpdate(BaseModel):
    phone: Optional[int] = Field(None, ge=1000000000, le=9999999999)
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, max_length=100)
    dob: Optional[date] = None
    status: Optional[UserStatus] = None

class AdminResponse(AdminBase):
    admin_id: str
    status: UserStatus
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Parent Models
class ParentBase(BaseModel):
    phone: int = Field(..., ge=1000000000, le=9999999999)
    email: Optional[EmailStr] = None
    name: str = Field(..., max_length=100)
    dob: Optional[date] = None
    parent_role: ParentRole = ParentRole.GUARDIAN
    door_no: Optional[str] = Field(None, max_length=50)
    street: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=50)
    district: Optional[str] = Field(None, max_length=50)
    state: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = Field(None, max_length=50)
    pincode: Optional[str] = Field(None, max_length=10)

class ParentCreate(ParentBase):
    password: str = Field(..., min_length=6, max_length=72)  # Password required for login

class ParentUpdate(BaseModel):
    phone: Optional[int] = Field(None, ge=1000000000, le=9999999999)
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, max_length=100)
    dob: Optional[date] = None
    parent_role: Optional[ParentRole] = None
    door_no: Optional[str] = Field(None, max_length=50)
    street: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=50)
    district: Optional[str] = Field(None, max_length=50)
    state: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = Field(None, max_length=50)
    pincode: Optional[str] = Field(None, max_length=10)
    parents_active_status: Optional[UserStatus] = None

class ParentResponse(ParentBase):
    parent_id: str
    parents_active_status: UserStatus = UserStatus.ACTIVE
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Driver Models
class DriverBase(BaseModel):
    name: str = Field(..., max_length=100)
    phone: int = Field(..., ge=1000000000, le=9999999999)
    email: Optional[EmailStr] = None
    dob: Optional[date] = None
    licence_number: Optional[str] = Field(None, max_length=50)
    licence_expiry: Optional[date] = None
    aadhar_number: Optional[str] = Field(None, max_length=20)
    licence_url: Optional[str] = Field(None, max_length=255)
    aadhar_url: Optional[str] = Field(None, max_length=255)
    photo_url: Optional[str] = Field(None, max_length=255)
    fcm_token: Optional[str] = Field(None, max_length=255)

class DriverCreate(DriverBase):
    password: str = Field(..., min_length=6, max_length=72)  # Password required for login

class DriverUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    phone: Optional[int] = Field(None, ge=1000000000, le=9999999999)
    email: Optional[EmailStr] = None
    dob: Optional[date] = None
    kyc_verified: Optional[bool] = None
    licence_number: Optional[str] = Field(None, max_length=50)
    licence_expiry: Optional[date] = None
    aadhar_number: Optional[str] = Field(None, max_length=20)
    licence_url: Optional[str] = Field(None, max_length=255)
    aadhar_url: Optional[str] = Field(None, max_length=255)
    photo_url: Optional[str] = Field(None, max_length=255)
    fcm_token: Optional[str] = Field(None, max_length=255)
    status: Optional[UserStatus] = None

class DriverResponse(DriverBase):
    driver_id: str
    kyc_verified: bool
    status: UserStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Route Models
class RouteBase(BaseModel):
    name: str = Field(..., max_length=100)

class RouteCreate(RouteBase):
    pass

class RouteUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    routes_active_status: Optional[UserStatus] = None

class RouteResponse(RouteBase):
    route_id: str
    routes_active_status: UserStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Bus Models
class BusBase(BaseModel):
    bus_number: str = Field(..., max_length=20)
    driver_id: Optional[str] = None
    route_id: Optional[str] = None
    bus_type: Optional[str] = Field(None, max_length=50)
    bus_brand: Optional[str] = Field(None, max_length=100)
    bus_model: Optional[str] = Field(None, max_length=100)
    seating_capacity: int = Field(..., gt=0)
    rc_expiry_date: Optional[date] = None
    fc_expiry_date: Optional[date] = None
    rc_book_url: Optional[str] = Field(None, max_length=255)
    fc_certificate_url: Optional[str] = Field(None, max_length=255)
    bus_front_url: Optional[str] = Field(None, max_length=255)
    bus_back_url: Optional[str] = Field(None, max_length=255)
    bus_left_url: Optional[str] = Field(None, max_length=255)
    bus_right_url: Optional[str] = Field(None, max_length=255)

class BusCreate(BusBase):
    pass

class BusUpdate(BaseModel):
    bus_number: Optional[str] = Field(None, max_length=20)
    driver_id: Optional[str] = None
    route_id: Optional[str] = None
    bus_type: Optional[str] = Field(None, max_length=50)
    bus_brand: Optional[str] = Field(None, max_length=100)
    bus_model: Optional[str] = Field(None, max_length=100)
    seating_capacity: Optional[int] = Field(None, gt=0)
    rc_expiry_date: Optional[date] = None
    fc_expiry_date: Optional[date] = None
    rc_book_url: Optional[str] = Field(None, max_length=255)
    fc_certificate_url: Optional[str] = Field(None, max_length=255)
    bus_front_url: Optional[str] = Field(None, max_length=255)
    bus_back_url: Optional[str] = Field(None, max_length=255)
    bus_left_url: Optional[str] = Field(None, max_length=255)
    bus_right_url: Optional[str] = Field(None, max_length=255)
    status: Optional[UserStatus] = None

class BusResponse(BusBase):
    bus_id: str
    status: UserStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Route Stop Models
class RouteStopBase(BaseModel):
    route_id: str
    stop_name: str = Field(..., max_length=100)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    stop_order: int

class RouteStopCreate(RouteStopBase):
    pass

class RouteStopUpdate(BaseModel):
    stop_name: Optional[str] = Field(None, max_length=100)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    stop_order: Optional[int] = None

class RouteStopResponse(RouteStopBase):
    stop_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Student Models
class StudentBase(BaseModel):
    parent_id: str
    s_parent_id: Optional[str] = None
    name: str = Field(..., max_length=100)
    dob: Optional[date] = None
    class_section: Optional[str] = Field(None, max_length=50)
    route_id: str
    pickup_stop_id: str
    drop_stop_id: str
    pickup_stop_order: int = Field(..., description="Order of pickup stop in route")
    drop_stop_order: int = Field(..., description="Order of drop stop in route")
    emergency_contact: Optional[int] = Field(None, ge=1000000000, le=9999999999)
    student_photo_url: Optional[str] = Field(None, max_length=200)

    @validator('drop_stop_id')
    def stops_different(cls, v, values):
        if v and 'pickup_stop_id' in values and v == values['pickup_stop_id']:
            raise ValueError('Pickup and drop stops must be different')
        return v
    
    @validator('drop_stop_order')
    def stop_order_valid(cls, v, values):
        if v and 'pickup_stop_order' in values and v <= values['pickup_stop_order']:
            raise ValueError('Drop stop order must be greater than pickup stop order')
        return v

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    parent_id: Optional[str] = None
    s_parent_id: Optional[str] = None
    name: Optional[str] = Field(None, max_length=100)
    dob: Optional[date] = None
    class_section: Optional[str] = Field(None, max_length=50)
    route_id: Optional[str] = None
    pickup_stop_id: Optional[str] = None
    drop_stop_id: Optional[str] = None
    pickup_stop_order: Optional[int] = None
    drop_stop_order: Optional[int] = None
    emergency_contact: Optional[int] = Field(None, ge=1000000000, le=9999999999)
    student_photo_url: Optional[str] = Field(None, max_length=200)
    student_status: Optional[StudentStatus] = None
    transport_status: Optional[TransportStatus] = None

class StudentResponse(StudentBase):
    student_id: str
    student_status: StudentStatus
    transport_status: TransportStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Trip Models
class TripBase(BaseModel):
    bus_id: str
    driver_id: str
    route_id: str
    trip_date: date
    trip_type: TripType

class TripCreate(TripBase):
    pass

class TripUpdate(BaseModel):
    status: Optional[TripStatus] = None
    current_stop_order: Optional[int] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

class TripResponse(TripBase):
    trip_id: str
    status: TripStatus
    current_stop_order: int
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Authentication Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    user_type: Optional[str] = None
    phone: Optional[int] = None

# Error Handling Models
class ErrorHandlingBase(BaseModel):
    error_type: Optional[str] = Field(None, max_length=50)
    error_code: Optional[int] = None
    error_description: Optional[str] = Field(None, max_length=255)

class ErrorHandlingCreate(ErrorHandlingBase):
    pass

class ErrorHandlingUpdate(BaseModel):
    error_type: Optional[str] = Field(None, max_length=50)
    error_code: Optional[int] = None
    error_description: Optional[str] = Field(None, max_length=255)

class ErrorHandlingResponse(ErrorHandlingBase):
    error_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Universal login model (phone + password)
class LoginRequest(BaseModel):
    phone: int = Field(..., description="10-digit phone number")
    password: str = Field(..., min_length=1, description="User password")
    
    @validator('phone')
    def validate_phone(cls, v):
        if not (1000000000 <= v <= 9999999999):
            raise ValueError('Phone number must be exactly 10 digits')
        return v
