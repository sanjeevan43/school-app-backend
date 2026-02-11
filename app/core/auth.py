from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import get_settings
from app.api.models import TokenData

settings = get_settings()
security = HTTPBearer(auto_error=False)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """Verify and decode JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not credentials:
        raise credentials_exception
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        user_type: str = payload.get("user_type")
        
        if user_id is None or user_type is None:
            raise credentials_exception
        
        token_data = TokenData(user_id=user_id, user_type=user_type)
        return token_data
    except JWTError:
        raise credentials_exception

def get_current_admin(token_data: TokenData = Depends(verify_token)) -> str:
    """Get current admin user from token"""
    if token_data.user_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return token_data.user_id

def get_current_parent(token_data: TokenData = Depends(verify_token)) -> str:
    """Get current parent user from token"""
    if token_data.user_type != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Parent access required"
        )
    return token_data.user_id

def get_current_driver(token_data: TokenData = Depends(verify_token)) -> str:
    """Get current driver user from token"""
    if token_data.user_type != "driver":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Driver access required"
        )
    return token_data.user_id

def get_current_user(token_data: TokenData = Depends(verify_token)) -> TokenData:
    """Get current user (admin, parent, or driver) from token"""
    return token_data
