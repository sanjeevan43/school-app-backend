# OTP Service for phone-based authentication
# In production, integrate with SMS gateway like Twilio, MSG91, or AWS SNS

import random
import string
from datetime import datetime, timedelta
from typing import Dict, Optional

# In-memory OTP storage (use Redis in production)
otp_storage: Dict[int, dict] = {}

class OTPService:
    """Service for generating and verifying OTPs"""
    
    OTP_LENGTH = 6
    OTP_VALIDITY_MINUTES = 5
    MAX_ATTEMPTS = 3
    
    @staticmethod
    def generate_otp() -> str:
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=OTPService.OTP_LENGTH))
    
    @staticmethod
    def send_otp(phone: int) -> dict:
        """
        Generate and send OTP to phone number
        In production, integrate with SMS gateway
        """
        otp = OTPService.generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=OTPService.OTP_VALIDITY_MINUTES)
        
        # Store OTP
        otp_storage[phone] = {
            'otp': otp,
            'expires_at': expires_at,
            'attempts': 0,
            'verified': False
        }
        
        # TODO: Send SMS via gateway
        # sms_gateway.send(phone, f"Your OTP is: {otp}. Valid for {OTPService.OTP_VALIDITY_MINUTES} minutes.")
        
        # For development, return OTP (remove in production)
        return {
            'message': 'OTP sent successfully',
            'phone': phone,
            'otp': otp,  # Remove this in production
            'expires_in_minutes': OTPService.OTP_VALIDITY_MINUTES
        }
    
    @staticmethod
    def verify_otp(phone: int, otp: str) -> bool:
        """Verify OTP for phone number"""
        if phone not in otp_storage:
            return False
        
        stored_data = otp_storage[phone]
        
        # Check if OTP expired
        if datetime.utcnow() > stored_data['expires_at']:
            del otp_storage[phone]
            return False
        
        # Check attempts
        if stored_data['attempts'] >= OTPService.MAX_ATTEMPTS:
            del otp_storage[phone]
            return False
        
        # Verify OTP
        if stored_data['otp'] == otp:
            stored_data['verified'] = True
            return True
        else:
            stored_data['attempts'] += 1
            return False
    
    @staticmethod
    def is_verified(phone: int) -> bool:
        """Check if phone number is verified"""
        if phone not in otp_storage:
            return False
        
        stored_data = otp_storage[phone]
        
        # Check if expired
        if datetime.utcnow() > stored_data['expires_at']:
            del otp_storage[phone]
            return False
        
        return stored_data.get('verified', False)
    
    @staticmethod
    def clear_otp(phone: int):
        """Clear OTP data for phone number"""
        if phone in otp_storage:
            del otp_storage[phone]
    
    @staticmethod
    def resend_otp(phone: int) -> dict:
        """Resend OTP to phone number"""
        # Clear existing OTP
        OTPService.clear_otp(phone)
        # Generate and send new OTP
        return OTPService.send_otp(phone)
