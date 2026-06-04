from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class FirewallMiddleware(BaseHTTPMiddleware):
    """
    Firewall middleware to block direct browser access and Swagger docs,
    allowing only approved websites and mobile apps to consume the API.
    """
    def __init__(self, app, allowed_origins: Optional[List[str]] = None):
        super().__init__(app)
        self.allowed_origins = allowed_origins or [
            "https://transport.selvagam.com",
            "https://selvagam-testing.web.app",
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:5174",
            "http://localhost:5175",
        ]

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        user_agent = request.headers.get("user-agent", "").lower()
        origin = request.headers.get("origin")
        referer = request.headers.get("referer", "")
        
        # 1. Block Swagger & OpenAPI Docs explicitly
        if path in ["/docs", "/redoc", "/openapi.json"]:
            logger.warning(f"Blocked attempt to access docs at {path}")
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "API Documentation is disabled."}
            )

        # 2. Block Direct Browser Access
        # Modern browsers send "Mozilla" in the User-Agent. 
        # If it's a browser, it must come from an allowed website (have Origin or Referer).
        is_browser = "mozilla" in user_agent or "chrome" in user_agent or "safari" in user_agent

        if is_browser:
            # Check if it's a valid CORS request or referred by our websites
            is_allowed_origin = False
            if origin and any(origin.startswith(allowed) for allowed in self.allowed_origins):
                is_allowed_origin = True
            elif referer and any(referer.startswith(allowed) for allowed in self.allowed_origins):
                is_allowed_origin = True
            
            if not is_allowed_origin:
                logger.warning(f"Blocked direct browser/unauthorized web access: UA={user_agent}, Origin={origin}")
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "Direct browser access or unauthorized origin is forbidden."}
                )

        # 3. Mobile Apps
        # Mobile apps (like Flutter, React Native, native Android/iOS) either don't use 
        # standard browser User-Agents, or they are handled by custom networking clients.
        # Since they bypass the `is_browser` check (or if they do have Mozilla, they need to pass a custom header in production),
        # they will proceed naturally.

        return await call_next(request)
