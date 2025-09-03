# User Authentication Module
import hashlib
from functools import wraps
from flask import request, jsonify

def authenticate_user(username, password):
    """Authenticate user credentials"""
    # Simple hash-based authentication (for demo)
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return username == "admin" and password_hash == "admin_hash"

def require_auth(f):
    """Authentication decorator"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not authenticate_user(auth.username, auth.password):
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated