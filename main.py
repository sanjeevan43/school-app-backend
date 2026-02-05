from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config import get_settings
from routes import router
import uvicorn
import logging

settings = get_settings()
logging.basicConfig(level=logging.INFO)

# Enhanced FastAPI app with comprehensive Swagger UI
app = FastAPI(
    title="🚌 School Transport Management API",
    description="""
    ## 🚌 School Transport Management System
    
    Complete API for managing school transport operations with password-based authentication.
    
    ### 🔐 Authentication
    - **Universal Login**: Phone number + Password for all user types
    - **JWT Tokens**: Secure authentication with role-based access
    
    ### 📊 Database Tables (ID First)
    - **🔧 Admins**: System administrators (admin_id, phone, email, name, status)
    - **👨‍👩‍👧‍👦 Parents**: Student guardians (parent_id, phone, email, name, parent_role, address)
    - **🚗 Drivers**: Bus drivers (driver_id, name, phone, email, licence_number, status)
    - **🛣️ Routes**: Bus routes (route_id, name, routes_active_status)
    - **🚌 Buses**: School buses (bus_id, registration_number, driver_id, route_id, status)
    - **🎓 Students**: Transport users (student_id, parent_id, name, class_id, transport_status)
    - **🏫 Classes**: School classes (class_id, class_name, section, academic_year)
    - **📍 Route Stops**: Bus stops (stop_id, route_id, stop_name, coordinates)
    - **🚌 Trips**: Daily journeys (trip_id, bus_id, driver_id, route_id, status)
    - **⚠️ Error Logs**: System errors (error_id, error_type, error_code)
    
    ### ✨ Key Features
    - **60+ REST Endpoints** with full CRUD operations
    - **Status Update Endpoints** for all entities (PUT /entity/{id}/status)
    - **ID Fields First** in all API responses
    - **Cascade Updates** for related data
    - **Real-time Bus Tracking** with FCM notifications
    - **Password-based Authentication** (no OTP required)
    
    ### 🔄 Status Update Examples
    ```bash
    # Update admin status
    PUT /api/v1/admins/{admin_id}/status
    {"status": "INACTIVE"}
    
    # Update student transport status
    PUT /api/v1/students/{student_id}/status
    {"status": "TEMP_STOP"}
    ```
    
    ### 🚀 Quick Start
    1. **Create Admin**: `POST /api/v1/admins`
    2. **Login**: `POST /api/v1/auth/login` (works for all user types)
    3. **Use Bearer Token**: Add to Authorization header for protected endpoints
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "Students", "description": "🎓 Student transport management (student_id first)"},
        {"name": "Parents", "description": "👨👩👧👦 Parent/guardian management (parent_id first)"},
        {"name": "Routes", "description": "🛣️ Bus route management (route_id first)"},
        {"name": "Route Stops", "description": "📍 Bus stop management (stop_id first)"},
        {"name": "Buses", "description": "🚌 School bus management (bus_id first)"},
        {"name": "Drivers", "description": "🚗 Bus driver management (driver_id first)"},
        {"name": "Admins", "description": "🔧 System administrator management (admin_id first)"},
        {"name": "Classes", "description": "🏫 School class management (class_id first)"},
        {"name": "Trips", "description": "🚌 Daily bus trip management (trip_id first)"},
        {"name": "Authentication", "description": "🔐 Login operations for all user types"},
        {"name": "Error Handling", "description": "⚠️ System error log management (error_id first)"},
        {"name": "Encryption", "description": "🔒 Data encryption services"},
        {"name": "FCM Tokens", "description": "📱 Push notification token management"},
        {"name": "Bus Tracking", "description": "📍 Real-time bus location tracking"}
    ],
        {"name": "Authentication", "description": "🔐 Login operations for all user types"},
        {"name": "Admins", "description": "🔧 System administrator management (admin_id first)"},
        {"name": "Parents", "description": "👨‍👩‍👧‍👦 Parent/guardian management (parent_id first)"},
        {"name": "Drivers", "description": "🚗 Bus driver management (driver_id first)"},
        {"name": "Routes", "description": "🛣️ Bus route management (route_id first)"},
        {"name": "Buses", "description": "🚌 School bus management (bus_id first)"},
        {"name": "Route Stops", "description": "📍 Bus stop management (stop_id first)"},
        {"name": "Classes", "description": "🏫 School class management (class_id first)"},
        {"name": "Students", "description": "🎓 Student transport management (student_id first)"},
        {"name": "Trips", "description": "🚌 Daily bus trip management (trip_id first)"},
        {"name": "Error Handling", "description": "⚠️ System error log management (error_id first)"},
        {"name": "Encryption", "description": "🔒 Data encryption services"},
        {"name": "FCM Tokens", "description": "📱 Push notification token management"},
        {"name": "Bus Tracking", "description": "📍 Real-time bus location tracking"}
    ],
    contact={
        "name": "School Transport API Support",
        "email": "admin@school.com",
    },
    license_info={
        "name": "MIT License",
    }
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=getattr(settings, 'ALLOWED_ORIGINS', ["http://localhost:3000", "http://localhost:8080"]),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1")

# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "🚌 School Transport Management API",
        "version": "1.0.0",
        "features": {
            "total_endpoints": "60+",
            "status_updates": "PUT /entity/{id}/status",
            "id_fields_first": "All responses show ID fields first",
            "authentication": "Password-based for all user types",
            "status_example": '{"status": "ACTIVE"}'
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health", include_in_schema=False)
async def health_check():
    try:
        from database import get_db
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected"}
        )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    import traceback
    
    # Log the actual error for debugging
    logging.error(f"Unhandled exception: {exc}")
    logging.error(f"Traceback: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DEBUG else "An error occurred",
            "path": str(request.url.path)
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )