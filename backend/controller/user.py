from flask import jsonify, url_for, request , session
from flask_jwt_extended import create_access_token , get_jwt_identity , decode_token
# from backend.models.farmer import Farmer
from models.farmer import Farmer
from models.user import User
from models import db
from extensions import oauth
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import ProgrammingError
from flask_mail import Message
from extensions import mail
from datetime import timedelta
import random
import string
import datetime
import json

bcrypt = Bcrypt()

def google_login():
    state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    session['state'] = state
    google = oauth.create_client('google')
    redirect_uri = url_for('auth.google_authorize_route', _external=True)
    print(f"Redirecting with state: {state}")
    print(f"State in session before redirect: {session['state']}")
    return google.authorize_redirect(redirect_uri, state=state)

def google_authorize():
    google = oauth.create_client('google')
    try:
        token = google.authorize_access_token()
    except Exception as e:
        return jsonify({'error': 'Failed to authorize access token', 'message': str(e)}), 400

    state_from_request = request.args.get('state')
    state_from_session = session.get('state')

    print(f"State from request: {state_from_request}")
    print(f"State from session: {state_from_session}")

    if state_from_request != state_from_session:
        return jsonify({'error': 'Invalid state parameter'}), 400
    
    try:
        resp = google.get('Farmerinfo')
        Farmer_info = resp.json()
    except Exception as e:
        return jsonify({'error': 'Failed to fetch Farmer info from Google', 'message': str(e)}), 400

    try:
        existing_user = Farmer.query.filter_by(google_id=Farmer_info['id']).first()
    except ProgrammingError:
        existing_user = None
 
    if not existing_user:
        new_Farmer = Farmer(
            email=Farmer_info['email'],
            google_id=Farmer_info['id'],
            Farmername=Farmer_info['name'],
            phone_no=None
        )
        db.session.add(new_Farmer)
        db.session.commit()

    access_token = create_access_token(
    identity=json.dumps({'id': new_Farmer.id, 'email': new_Farmer.email}),  
    expires_delta=datetime.timedelta(minutes=10),
    fresh=True
    )

    return jsonify({'access_token': access_token, 'Farmer': new_Farmer.__repr__()}), 200

def signup():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        role = data.get('role')  # either "user" or "farmer"

        if not email or not password or not username or not role:
            return jsonify({'Error': 'Some fields are missing'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        if role.lower() == 'farmer':
            existing_user = Farmer.query.filter_by(email=email).first()
        elif role.lower() == 'user':
            existing_user = User.query.filter_by(email=email).first()
        else:
            return jsonify({'Error': 'Invalid role. Choose either "user" or "farmer"'}), 400

        if existing_user:
            return jsonify({'Error': f'{role.capitalize()} with this email already exists'}), 400

        if role.lower() == 'farmer':
            new_user = Farmer(email=email, password=hashed_password, username=username)
        else:
            new_user = User(email=email, password=hashed_password, username=username)

        db.session.add(new_user)
        db.session.commit()

        # JWT token
        access_token = create_access_token(
        identity=json.dumps({'id': new_user.id, 'email': new_user.email,'role':role}),  
        expires_delta=datetime.timedelta(minutes=10),
        fresh=True
        )

        return jsonify({'access_token': access_token, 'Farmer': new_user.__repr__()}), 200

    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    
def login():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        role = data.get('role') 

        if not email or not password or not role:
            return jsonify({"Error": "Email, password, and role are required"}), 400

        if role.lower() == 'farmer':
            existing_user = Farmer.query.filter_by(email=email).first()
        elif role.lower() == 'user':
            existing_user = User.query.filter_by(email=email).first()
        else:
            return jsonify({'Error': 'Invalid role. Choose either "user" or "farmer"'}), 400

        if not existing_user:
            return jsonify({"Error": f"{role.capitalize()} does not exist"}), 404

        # Check if registered via Google and prevent manual login
        if hasattr(existing_user, 'google_id') and existing_user.google_id:
            return jsonify({"Error": "This email is registered via Google. Use Google Login."}), 403

        if not bcrypt.check_password_hash(existing_user.password, password):
            return jsonify({"Error": "Password is incorrect"}), 401

        access_token = create_access_token(
        identity=json.dumps({'id': existing_user.id, 'email': existing_user.email,'role':role}),  
        expires_delta=datetime.timedelta(minutes=10),
        fresh=True
        ) 

        return jsonify({'access_token': access_token, 'Farmer': existing_user.__repr__()}), 200

    except Exception as e:
        return jsonify({'Error': str(e)}), 500

def get_user():
    try:
        identity_str = get_jwt_identity()
        identity = json.loads(identity_str)

        user_id = identity.get("id")
        role = identity.get("role")

        if not user_id or not role:
            return jsonify({"message": "Invalid token data"}), 401

        if role == "Farmer":
            user = Farmer.query.get(user_id)
        elif role == "User":
            user = User.query.get(user_id)
        else:
            return jsonify({"message": "Invalid role"}), 403

        if user is None:
            return jsonify({"message": "User not found"}), 404

        return jsonify({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'phone_no': getattr(user, 'phone_no', None) 
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
def update_user():
    try:
        identity_str = get_jwt_identity()
        identity = json.loads(identity_str)

        user_id = identity.get("id")
        role = identity.get("role")

        if not user_id or not role:
            return jsonify({"message": "Invalid token data"}), 401

        role = role.lower()

        if role == "farmer":
            user = Farmer.query.get(user_id)
        elif role == "user":
            user = User.query.get(user_id)
        else:
            return jsonify({"message": "Invalid role"}), 403

        if user is None:
            return jsonify({"message": "User not found"}), 404

        data = request.get_json()

        if 'email' in data:
            user.email = data['email']
        if 'username' in data:
            user.username = data['username']
        if 'phone_no' in data:
            user.phone_no = data['phone_no']
        if 'age' in data and role == "farmer":
            user.age = data['age']

        db.session.commit()

        return jsonify({
            'message': f'{role.capitalize()} updated successfully',
            role: {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'phone_no': getattr(user, 'phone_no', None),
                'age': getattr(user, 'age', None) if role == "farmer" else None
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_user():
    identity_str = get_jwt_identity()
    identity = json.loads(identity_str)

    current_Farmer_id = identity.get("id")
    if not current_Farmer_id:
        return jsonify({"message": "Invalid token data"}), 401
    
    existing_Farmer = Farmer.query.get(current_Farmer_id)

    if existing_Farmer is None:
        return jsonify({"message": "Farmer not found"}), 404
    
    db.session.delete(existing_Farmer)
    db.session.commit()

    return jsonify({"message": "Farmer deleted successfully"}), 200

def generate_reset_token(email,id):

    reset_token = create_access_token(
    identity=json.dumps({'id': id, 'email': email}),  
    expires_delta=datetime.timedelta(hours=1)
    )
    return reset_token


def verify_reset_token(token):
    try:
        decoded_token = decode_token(token)
        identity_str = decoded_token['sub']  
        identity = json.loads(identity_str) 
        email = identity['email']
        return email
    except Exception as e:
        print(f"Token decoding error: {e}")
        return None

def send_email(to_email,subject,body):
    msg = Message(subject,recipients=[to_email])
    msg.body = body
    mail.send(msg)

def update_password():
    try:
        data = request.get_json()

        if data is None:
            return jsonify({'Error': 'Invalid or missing JSON'}), 400

        email = data.get("email")
        role = data.get("role")

        if not email or not role:
            return jsonify({'Error': 'Email and role are required'}), 400

        role = role.lower()

        if role == "farmer":
            existing_user = Farmer.query.filter_by(email=email).first()
        elif role == "user":
            existing_user = User.query.filter_by(email=email).first()
        else:
            return jsonify({'Error': 'Invalid role'}), 400

        if not existing_user:
            return jsonify({'Error': 'Email not found'}), 404

        if not existing_user.password or existing_user.password.strip() == "":
            return jsonify({'Error': 'This email is linked to Google Login. Use Google to sign in.'}), 400

        # token with email and user ID
        token = generate_reset_token(email, existing_user.id)
        print("Generated reset token:", token)

        # Reset link
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        print("Generated reset URL:", reset_url)

        subject = "Password Reset Request"
        message = f"Click the link to reset your password: {reset_url}. If you did not request this, ignore this email."

        send_email(email, subject, message)

        return jsonify({'message': 'A password reset link has been sent to your email address. Please check your inbox and reset your password.'}), 200

    except Exception as e:
        return jsonify({'Error': str(e)}), 500


def reset(token):
    try:
        email = verify_reset_token(token)
        if not email:
            return jsonify({'Error': 'Invalid or expired token'}), 400
        
        new_password = request.json.get('new_password')
        if not new_password:
            return jsonify({'Error':'New password is required'}), 400
        
        existing_Farmer = Farmer.query.filter_by(email=email).first()
        if not existing_Farmer:
            return jsonify({'Error':'Farmer not found'}), 400
        
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        existing_Farmer.password = hashed_password
        db.session.commit()

        return jsonify({'Message': 'Password updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'ErrorHum': str(e)}), 400