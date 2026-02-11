import base64
from cryptography.fernet import Fernet
from config import get_settings
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

# Generate a key for encryption (in production, store this securely)
def generate_key():
    return Fernet.generate_key()

# Use a fixed key for demo (in production, use environment variable)
ENCRYPTION_KEY = base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32].ljust(32, b'0'))

def encrypt_data(data: str) -> str:
    """Encrypt string data"""
    try:
        f = Fernet(ENCRYPTION_KEY)
        encrypted_data = f.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        return data  # Return original data if encryption fails

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt string data"""
    try:
        f = Fernet(ENCRYPTION_KEY)
        decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = f.decrypt(decoded_data)
        return decrypted_data.decode()
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        return encrypted_data  # Return original data if decryption fails