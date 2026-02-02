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
    CANCELED = "CANCELED"

# Admin Models
class AdminBase(BaseModel):
    phone: int = Field(..., ge=1000000000, le=9999999999)
    email: Optional[EmailStr] = None
    name: str = Field(..., max_length=100)

class AdminCreate(AdminBase):
    password: str = Field(..., min_length=6, max_length=72)

class AdminUpdate(BaseModel):
    phone: Optional[int] = Field(None, ge=1000000000, le=9999999999)
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, max_length=100)
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
    parent_role: ParentRole = ParentRole.GUARDIAN
    door_no: Optional[str] = Field(None, max_length=50)
    street: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=50)
    district: Optional[str] = Field(None, max_length=50)
    pincode: Optional[str] = Field(None, max_length=10)

class ParentCreate(ParentBase):
    password: str = Field(..., min_length=6, max_length=72)  # Password required for login

class ParentUpdate(BaseModel):
    phone: Optional[int] = Field(None, ge=1000000000, le=9999999999)
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, max_length=100)
    parent_role: Optional[ParentRole] = None
    door_no: Optional[str] = Field(None, max_length=50)
    street: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=50)
    district: Optional[str] = Field(None, max_length=50)
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
    licence_number: Optional[str] = Field(None, max_length=50)
    licence_expiry: Optional[date] = None
    fcm_token: Optional[str] = Field(None, max_length=255)

class DriverCreate(DriverBase):
    password: str = Field(..., min_length=6, max_length=72)  # Password required for login

class DriverUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    phone: Optional[int] = Field(None, ge=1000000000, le=9999999999)
    email: Optional[EmailStr] = None
    licence_number: Optional[str] = Field(None, max_length=50)
    licence_expiry: Optional[date] = None
    fcm_token: Optional[str] = Field(None, max_length=255)
    status: Optional[UserStatus] = None

class DriverResponse(DriverBase):
    driver_id: str
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
    registration_number: str = Field(..., max_length=20)
    driver_id: Optional[str] = None
    route_id: Optional[str] = None
    vehicle_type: Optional[str] = Field(None, max_length=50)
    bus_brand: Optional[str] = Field(None, max_length=100)
    bus_model: Optional[str] = Field(None, max_length=100)
    seating_capacity: int = Field(..., gt=0)
    rc_expiry_date: Optional[date] = None
    fc_expiry_date: Optional[date] = None
    rc_book_url: Optional[str] = Field(None, max_length=255)
    fc_certificate_url: Optional[str] = Field(None, max_length=255)

class BusCreate(BusBase):
    pass

class BusUpdate(BaseModel):
    registration_number: Optional[str] = Field(None, max_length=20)
    driver_id: Optional[str] = None
    route_id: Optional[str] = None
    vehicle_type: Optional[str] = Field(None, max_length=50)
    bus_brand: Optional[str] = Field(None, max_length=100)
    bus_model: Optional[str] = Field(None, max_length=100)
    seating_capacity: Optional[int] = Field(None, gt=0)
    rc_expiry_date: Optional[date] = None
    fc_expiry_date: Optional[date] = None
    rc_book_url: Optional[str] = Field(None, max_length=255)
    fc_certificate_url: Optional[str] = Field(None, max_length=255)
    status: Optional[UserStatus] = None

class BusResponse(BusBase):
    bus_id: str
    status: UserStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Class Models
class ClassBase(BaseModel):
    class_name: str = Field(..., max_length=20)
    section: str = Field(..., max_length=10)
    academic_year: str = Field(..., max_length=20)

class ClassCreate(ClassBase):
    pass

class ClassUpdate(BaseModel):
    class_name: Optional[str] = Field(None, max_length=20)
    section: Optional[str] = Field(None, max_length=10)
    academic_year: Optional[str] = Field(None, max_length=20)
    status: Optional[UserStatus] = None

class ClassResponse(ClassBase):
    class_id: str
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
    pickup_stop_order: int
    drop_stop_order: int

class RouteStopCreate(RouteStopBase):
    pass

class RouteStopUpdate(BaseModel):
    stop_name: Optional[str] = Field(None, max_length=100)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    pickup_stop_order: Optional[int] = None
    drop_stop_order: Optional[int] = None

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
    class_id: Optional[str] = None
    pickup_route_id: str
    drop_route_id: str
    pickup_stop_id: str
    drop_stop_id: str
    emergency_contact: Optional[int] = Field(None, ge=1000000000, le=9999999999)
    student_photo_url: Optional[str] = Field(None, max_length=200)

    @validator('drop_stop_id')
    def stops_different(cls, v, values):
        if v and 'pickup_stop_id' in values and v == values['pickup_stop_id']:
            raise ValueError('Pickup and drop stops must be different')
        return v

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    parent_id: Optional[str] = None
    s_parent_id: Optional[str] = None
    name: Optional[str] = Field(None, max_length=100)
    dob: Optional[date] = None
    class_id: Optional[str] = None
    pickup_route_id: Optional[str] = None
    drop_route_id: Optional[str] = None
    pickup_stop_id: Optional[str] = None
    drop_stop_id: Optional[str] = None
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

# FCM Token Models
class FCMTokenBase(BaseModel):
    fcm_token: str = Field(..., max_length=255)
    student_id: Optional[str] = None
    parent_id: Optional[str] = None

class FCMTokenCreate(FCMTokenBase):
    pass

class FCMTokenUpdate(BaseModel):
    fcm_token: Optional[str] = Field(None, max_length=255)
    student_id: Optional[str] = None
    parent_id: Optional[str] = None

class FCMTokenResponse(FCMTokenBase):
    fcm_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Bus Location Models
class BusLocationUpdate(BaseModel):
    trip_id: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timestamp: Optional[datetime] = None

class NotificationRequest(BaseModel):
    trip_id: str
    message: str
    stop_id: Optional[str] = None

# Universal login model (phone + password)
class LoginRequest(BaseModel):
    phone: int = Field(..., description="10-digit phone number")
    password: str = Field(..., min_length=1, description="User password")
    
    @validator('phone')
    def validate_phone(cls, v):
        if not (1000000000 <= v <= 9999999999):
            raise ValueError('Phone number must be exactly 10 digits')
        return v
