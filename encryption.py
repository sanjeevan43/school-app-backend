from cryptography.fernet import Fernet
from config import get_settings
import base64

settings = get_settings()

# Generate encryption key from SECRET_KEY
def get_encryption_key():
    key = base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32].ljust(32, b'0'))
    return key

def encrypt_data(data: str) -> str:
    """Encrypt string data"""
    f = Fernet(get_encryption_key())
    encrypted = f.encrypt(data.encode())
    return base64.urlsafe_b64encode(encrypted).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt string data"""
    f = Fernet(get_encryption_key())
    decoded = base64.urlsafe_b64decode(encrypted_data.encode())
    decrypted = f.decrypt(decoded)
    return decrypted.decode()