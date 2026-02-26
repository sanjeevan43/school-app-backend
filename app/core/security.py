import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash using bcrypt"""
    try:
        if not hashed_password:
            return False
            
        # Ensure we have bytes for comparison
        password_bytes = plain_password.encode('utf-8')
        
        # If hash is already bytes, use it, otherwise encode it
        if isinstance(hashed_password, str):
            hash_bytes = hashed_password.encode('utf-8')
        else:
            hash_bytes = hashed_password
            
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Generate a high-security bcrypt hash of the password with salt"""
    # bcrypt generates a random salt automatically
    # Returns the hash as a UTF-8 string to be stored in the database
    return bcrypt.hashpw(
        password.encode('utf-8'), 
        bcrypt.gensalt()
    ).decode('utf-8')
