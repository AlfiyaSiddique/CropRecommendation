from flask import jsonify, url_for, request , session
from flask_jwt_extended import create_access_token , get_jwt_identity , decode_token
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


bcrypt = Bcrypt()

def google_login():
    state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    session['state'] = state
    google = oauth.create_client('google')
    redirect_uri = url_for('auth.google_authorize', _external=True)
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
        resp = google.get('userinfo')
        user_info = resp.json()
    except Exception as e:
        return jsonify({'error': 'Failed to fetch user info from Google', 'message': str(e)}), 400

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

    print("getted signup")

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

    access_token = create_access_token(identity={'id': user.id, 'email': user.email} )

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

    access_token = create_access_token(identity={'id': user.id, 'email': user.email}, expires_delta=datetime.timedelta(minutes=10),fresh=True) 
    
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

def generate_reset_token(email):
    reset_token = create_access_token(identity={'email': email}, expires_delta=timedelta(hours=1))
    return reset_token


def verify_reset_token(token):
    try:
        decoded_token = decode_token(token)
        email = decoded_token['sub']['email']
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

        print (email)

        if not email:
            return jsonify({'Error': 'Some fields are missing'}), 400
        
        
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({'Error': 'Email not found'}), 404

        print(user)
        
        if not user.password or user.password.strip() == "":
            return jsonify({'Error': 'This email is linked to Google Login. Use Google to sign in.'}), 400
        
        token = generate_reset_token(email) 
        print("Humaira here is token")  
        print(token)

        # reset link
        reset_url = url_for('auth.reset_password', token=token, _external=True)

        print("Humaira reseset url")
        print(reset_url)

        subject = "Password Reset Request"
        message = f"Click the link to reset your password: {reset_url}. If you did not request this, ignore this email."
        
        send_email(email,subject,message)

        return jsonify({'message': 'A password reset link has been sent to your email address. Please check your inbox and reset your password.'}), 200

     
    except Exception as e:
        return jsonify({'ErrorHumaira': str(e)}), 400

def reset(token):
    try:
        email = verify_reset_token(token)
        if not email:
            return jsonify({'Error': 'Invalid or expired token'}), 400
        
        new_password = request.json.get('new_password')
        if not new_password:
            return jsonify({'Error':'New password is required'}), 400
        
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'Error':'User not found'}), 400
        
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        return jsonify({'Message': 'Password updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'ErrorHum': str(e)}), 400