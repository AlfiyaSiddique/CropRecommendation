from flask import Blueprint
from controller.user import google_login, google_authorize, signup, login, get_user, update_user, delete_user
from flask_jwt_extended import jwt_required
from flask import request

auth_bp = Blueprint('auth', __name__)
auth_bp.route("/login/google", methods=['GET'])(google_login)
auth_bp.route('/authorize', methods=['GET'])(google_authorize)

# email-based authentication routes
auth_bp.route('/signup', methods=['POST'])(signup)
auth_bp.route("/login", methods=['POST'])(login)

# user profile 
@auth_bp.route("/user",methods=['GET','PUT','DELETE'])
@jwt_required()
def user_profile():
    if request.method == 'GET':
        return get_user()
    elif request.method == 'PUT':
        return update_user()
    elif request.method == 'DELETE':
        return delete_user()
