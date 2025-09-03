# Security Patches
import re

def sanitize_input(input_string):
    """Sanitize user input to prevent injection attacks"""
    if not isinstance(input_string, str):
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', input_string)
    return sanitized.strip()

def validate_request_size(content_length, max_size=1024):
    """Validate request size to prevent DoS attacks"""
    if content_length > max_size:
        raise ValueError(f"Request too large: {content_length} > {max_size}")
    return True
