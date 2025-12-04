"""
Security utilities module
Implements additional security helper functions
"""
import re
from flask import request
import logging

logger = logging.getLogger(__name__)


def sanitize_input(input_string):
    """
    Sanitize user input to prevent XSS and injection attacks
    
    Args:
        input_string (str): User input to sanitize
        
    Returns:
        str: Sanitized input
    """
    if not isinstance(input_string, str):
        return input_string
    
    # Remove potentially dangerous characters
    sanitized = input_string.strip()
    
    # Remove script tags and other potentially harmful HTML
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
    sanitized = re.sub(r'<iframe[^>]*>.*?</iframe>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
    
    return sanitized


def log_security_event(event_type, user_id=None, details=None):
    """
    Log security-related events without exposing sensitive data
    
    Args:
        event_type (str): Type of security event
        user_id (int): User ID (if applicable)
        details (str): Additional non-sensitive details
    """
    ip_address = request.remote_addr if request else 'Unknown'
    
    log_message = f"Security Event: {event_type} | IP: {ip_address}"
    if user_id:
        log_message += f" | User ID: {user_id}"
    if details:
        log_message += f" | Details: {details}"
    
    logger.warning(log_message)


def validate_password_strength(password):
    """
    Validate password strength beyond basic requirements
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    # Check for common weak passwords
    common_passwords = ['password', '12345678', 'qwerty', 'abc123']
    if password.lower() in common_passwords:
        return False, "Password is too common. Please choose a stronger password"
    
    return True, "Password is strong"


def get_client_ip():
    """
    Get client IP address safely
    
    Returns:
        str: Client IP address
    """
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
    return request.environ.get('REMOTE_ADDR', 'Unknown')
