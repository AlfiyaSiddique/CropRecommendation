from flask import Blueprint, jsonify, request
from controller.user import google_login, google_authorize, signup, login, get_user, update_user, delete_user, update_password, reset
from flask_jwt_extended import jwt_required
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/auth/google/login", methods=['GET'])
def google_login_route():
    try:
        return google_login()
    except Exception as e:
        logger.error(f"Error in google_login: {str(e)}")
        return jsonify({'error': 'Google login failed'}), 500

@auth_bp.route('/auth/google/authorize', methods=['GET'])
def google_authorize_route():
    try:
        return google_authorize()
    except Exception as e:
        logger.error(f"Error in google_authorize: {str(e)}")
        return jsonify({'error': 'Google authorization failed'}), 500

# Email-based authentication routes
@auth_bp.route('/auth/signup', methods=['POST'])
def signup_route():
    try:
        return signup()
    except Exception as e:
        logger.error(f"Error in signup: {str(e)}")
        return jsonify({'error': 'Signup failed'}), 500

@auth_bp.route("/auth/login", methods=['POST'])
def login_route():
    try:
        return login()
    except Exception as e:
        logger.error(f"Error in login: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

# User profile
@auth_bp.route("/profile", methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def user_profile():
    try:
        if request.method == 'GET':
            return get_user()
        elif request.method == 'PUT':
            return update_user()
        elif request.method == 'DELETE':
            return delete_user()
    except Exception as e:
        logger.error(f"Error in user_profile: {str(e)}")
        return jsonify({'error': 'User profile operation failed'}), 500

auth_bp.route("/password/update", methods=['POST'])(update_password)

@auth_bp.route('/reset_password/<token>',methods=['POST'],endpoint='reset_password')
def reset_password(token):
        return reset(token)