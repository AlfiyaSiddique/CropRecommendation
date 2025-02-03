from flask import jsonify, url_for, request
from flask_jwt_extended import create_access_token
from models.user import User
from models import db
from extensions import oauth
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import ProgrammingError
from flask_jwt_extended import jwt_required, get_jwt_identity

bcrypt = Bcrypt()

def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth.google_authorize', _external=True) 
    return google.authorize_redirect(redirect_uri)

def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()

    try:
        user = User.query.filter_by(google_id=user_info['id']).first()
    except ProgrammingError:
        user = None

    if not user:
        user = User(
            email=user_info['email'],
            google_id=user_info['id'],
            username=user_info['name'],
            phone_no=None
        )
        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(identity={'id': user.id, 'email': user.email})

    return jsonify({'access_token': access_token, 'user': user.__repr__()}), 200

def signup():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    if not email or not password or not username:
        return jsonify({'Error': 'Some fields are missing'}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({'Error': 'User with this email already exists'}), 400
    
    user = User(
        email=email,
        password=hashed_password,
        username=username,
    )
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity={'id': user.id, 'email': user.email})

    return jsonify({'access_token': access_token, 'user': user.__repr__()}), 200

def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"Error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"Error": "User does not exist"}), 404
    
    if user.google_id:
        return jsonify({"Error": "This email is registered via Google. Use Google Login."}), 403

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"Error": "Password is incorrect"}), 401

    access_token = create_access_token(identity={'id': user.id, 'email': user.email})
    
    return jsonify({'access_token': access_token, 'user': user.__repr__()}), 200

def get_user():
    current_user_id = get_jwt_identity()['id']
    
    user = User.query.get(current_user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'phone_no': user.phone_no
    }), 200

def update_user():
    current_user_id = get_jwt_identity()['id']
    user = User.query.get(current_user_id)

    if user is None:
        return jsonify({"message": "User not found"}), 404
    
    data = request.get_json()
    
    if 'email' in data:
        user.email = data['email']
    if 'username' in data:
        user.username = data['username']
    if 'phone_no' in data:
        user.phone_no = data['phone_no']

    if 'age' in data:
        user.age = data['age']
    
    db.session.commit()

    return jsonify({
        'message': 'User updated successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'phone_no': user.phone_no
        }
    }), 200

def delete_user():
    current_user_id = get_jwt_identity()['id']
    user = User.query.get(current_user_id)

    if user is None:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200