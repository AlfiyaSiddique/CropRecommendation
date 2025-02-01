from flask import Blueprint
from controller.user import google_login, google_authorize, signup, login, get_user, update_user, delete_user
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__)
auth_bp.route("/login/google", methods=['GET'])(google_login)
auth_bp.route('/authorize', methods=['GET'])(google_authorize)

# email-based authentication routes
auth_bp.route('/signup', methods=['POST'])(signup)
auth_bp.route("/login", methods=['POST'])(login)

# user profile routes
@auth_bp.route("/user", methods=['GET'])
@jwt_required()
def protected_get_user():
    return get_user()

@auth_bp.route("/user", methods=['PUT'])
@jwt_required()
def protected_put_user():
    return update_user()

@auth_bp.route("/user", methods=['DELETE'])
@jwt_required()
def protected_delete_user():
    return delete_user()
