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
    title="School Transport Management API",
    description="""
    ## School Transport Management API
    
    ### Authentication
    - **All Users**: Phone number + Password login
    
    ### Features
    - **Complete CRUD operations** for all entities
    - **8 Entities**: Admins, Parents, Drivers, Routes, Buses, Route Stops, Students, Trips
    - **JWT Authentication** with role-based access
    - **Password-based authentication** for all user types
    
    ### Quick Start
    1. Create admin: `POST /api/v1/admins`
    2. Login: `POST /api/v1/auth/login` (works for all user types)
    3. Use Bearer token for authenticated endpoints
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "Authentication", "description": "Login operations"},
        {"name": "Admins", "description": "Admin management"},
        {"name": "Parents", "description": "Parent management"},
        {"name": "Drivers", "description": "Driver management"},
        {"name": "Routes", "description": "Route management"},
        {"name": "Buses", "description": "Bus management"},
        {"name": "Route Stops", "description": "Bus stop management"},
        {"name": "Classes", "description": "Class management"},
        {"name": "Students", "description": "Student management"},
        {"name": "Trips", "description": "Trip management"},
        {"name": "Error Handling", "description": "Error log management"},
        {"name": "Encryption", "description": "Data encryption services"}
    ],
    contact={
        "name": "School Transport API",
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
        "message": "School Transport Management API",
        "version": "1.0.0",
        "docs": "/docs"
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