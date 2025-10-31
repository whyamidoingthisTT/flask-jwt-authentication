#this is a protection decorators file containing 2 functions:
# 1. token_req -> protect routes (secturity guard)
# 2. admin_req -> protect adminn routes (vip security)

from flask import request, jsonify, current_app
from functools import wraps
from utils import verify_token
import os

def token_req(f):
    """
    Decorator to protect routes
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        #getting token from authorization header
        token = request.headers.get('Authorization')

        #check existance
        if not token:
            return jsonify({
                'message': 'Token is missing! Please login first.',
                'status': 'error'
            }), 401
        
        #extracting token from "Bearer <token>" format
        if token.startswith('Bearer '):
            token = token[7:] #"Bearer" prefix removed

        #getting secret key from app config (passed via kwargs)
        secret_key = os.getenv('SECRET_KEY')
        if not secret_key:
            return jsonify({
                'message': 'Server configuration error',
                'status': 'error'
                }), 500
        
        #verify token (this is where we call verify_token from utils)
        user_data = verify_token(token, secret_key)
        if not user_data:
            return jsonify({
                'message': 'Token is invalid or expired! Please login again.',
                'status': 'error'
            }), 401
        #when token valid pass user_data to protected fun
        return f(user_data, *args, **kwargs)
    return decorated

def admin_req(f):
    """
    Decorator for admin-only routes
    
    Usage:
        @admin_required
        def admin_route(user_data):
            # user_data contains admin info
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        #checking if token valid usin token_req
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message':'Token missing'}), 401
        if token.startswith('Bearer'):
            token = token[7:]

        secret_key = kwargs.get('secret_key')
        user_data = verify_token(token, secret_key)

        if not user_data:
            return jsonify({'message':'Invalid token'}), 401
        
        #verify if admin
        if user_data.get('role') != 'admin': #customizable
            return jsonify({
                'message': 'Admin access required!',
                'status': 'error'
            }), 403
        
        return f(user_data, *args, **kwargs)
    
    return decorated

