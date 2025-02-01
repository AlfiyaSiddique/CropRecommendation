from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            # can also retrieve the user identity
            current_user = get_jwt_identity()
        except Exception as e:
            return jsonify({"Error": "Authentication required"}), 401
        
        # Proceed to the original route function if the token is valid
        return fn(*args, **kwargs)

    return wrapper