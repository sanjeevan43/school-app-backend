from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.core.config import get_settings
import uvicorn
import os
import logging
import secrets
import asyncio
from app.services.cleanup_service import cleanup_service
from app.core.firewall import FirewallMiddleware
settings = get_settings()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="School Transport Management API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    openapi_tags=[
        {"name": "Dashboard", "description": "System statistics and analytics"},
        {"name": "Authentication", "description": "Login and authentication"},
        {"name": "Admins", "description": "System administrators"},
        {"name": "Parents", "description": "Parent/guardian management"},
        {"name": "Drivers", "description": "Bus driver management"},
        {"name": "Students", "description": "Student transport management"},
        {"name": "Buses", "description": "School bus management"},
        {"name": "Routes", "description": "Bus route management"},
        {"name": "Route Stops", "description": "Bus stop management"},
        {"name": "Classes", "description": "School class management"},
        {"name": "Trips", "description": "Daily bus trip management"},
        {"name": "Bus Tracking", "description": "Real-time bus tracking"},
        {"name": "Proximity Alerts", "description": "Advanced geofence-based notification logic"},
        {"name": "FCM Tokens", "description": "Push notifications"},
        {"name": "Error Handling", "description": "Error logs"}
    ],
    contact={
        "name": "API Support",
        "email": "admin@school.com",
    }
)

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = settings.DOCS_USERNAME.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = settings.DOCS_PASSWORD.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(get_current_username)):
    return get_redoc_html(openapi_url="/openapi.json", title="redoc")

@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return JSONResponse(app.openapi())

# Configure CORS
origins = [
    "https://transport.selvagam.com",
    "https://selvagam-testing.web.app",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add our custom FirewallMiddleware
app.add_middleware(FirewallMiddleware, allowed_origins=origins)

from fastapi.staticfiles import StaticFiles

from app.api.routes import router as main_router
from app.api.notification_routes import router as notification_router

# Include routers
app.include_router(main_router, prefix="/api/v1")
app.include_router(notification_router, prefix="/api/v1")

# Create upload directory if it doesn't exist
if not os.path.exists(settings.UPLOAD_DIR):
    os.makedirs(settings.UPLOAD_DIR)

# Mount static files
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Background Task for daily cleanup
async def scheduled_cleanup():
    """Run data pruning every 24 hours"""
    while True:
        try:
            logger.info("Triggering scheduled data pruning...")
            cleanup_service.prune_old_data(days=30)
        except Exception as e:
            logger.error(f"Scheduled cleanup error: {e}")
        
        # Wait for 24 hours (86400 seconds)
        await asyncio.sleep(86400)

@app.on_event("startup")
async def on_startup():
    """Actions to perform on startup"""
    # Start the background cleanup task
    asyncio.create_task(scheduled_cleanup())
    logger.info("Startup complete: Scheduled cleanup task started.")

# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "School Transport Management API",
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
        from app.core.database import get_db
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
