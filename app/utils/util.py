import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify, current_app

def encode_token(customer_id):
    SECRET_KEY = current_app.config['SECRET_KEY']
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': customer_id
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        SECRET_KEY = current_app.config['SECRET_KEY']
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        
        if not token:
            print("DEBUG: No token found in request")  # ADD THIS
            return jsonify({'message': 'Missing token'}), 401
        
        try:
            print(f"DEBUG: Attempting to decode token with SECRET_KEY: {SECRET_KEY[:10]}...")  # ADD THIS
            data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            customer_id = data['sub']
            print(f"DEBUG: Successfully decoded token for customer_id: {customer_id}")  # ADD THIS
        except jwt.ExpiredSignatureError as e:
            print(f"DEBUG: Token expired: {e}")  # ADD THIS
            return jsonify({'message': 'token expired'}), 401
        except jwt.InvalidTokenError as e:
            print(f"DEBUG: Invalid token: {e}")  # ADD THIS
            return jsonify({'message': 'Invalid token'}), 401
        except Exception as e:
            print(f"DEBUG: Unexpected error: {type(e).__name__}: {e}")  # ADD THIS
            return jsonify({'message': 'Token validation error'}), 401
        
        return f(customer_id, *args, **kwargs)
    
    return decorated
