from flask import Flask, request, jsonify
import joblib
import numpy as np
from dotenv import load_dotenv
import os
from models import db , User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from extensions import oauth , init_oauth
from routes.user import auth_bp
from controller.user import bcrypt
from datetime import timedelta
from extensions import init_mail
from flask import session
from flask_session import Session
from flask_cors import CORS

load_dotenv()

model = joblib.load('./modules/crop_recommendation_model.pkl')

app = Flask(__name__)

bcrypt.init_app(app)
CORS(app)

#Database Configuration:
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=2)

#Initialize SQLAlchemy
db.init_app(app)
jwt = JWTManager(app)

app.secret_key = os.getenv('APP_SECRET_KEY')

# Initialize extensions
migrate = Migrate(app, db)
jwt.init_app(app)
oauth.init_app(app)

# Initialize Google OAuth
init_oauth(app)

#mail configuration
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'team.cropxpert@gmail.com'
app.config['MAIL_PASSWORD'] = 'qqqa vvvt emkm lzxa'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'team.cropxpert@gmail.com'
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')

init_mail(app)

# Register blueprints (user-auth route)
app.register_blueprint(auth_bp)

@app.route('/', methods=['GET'])
def welcome():
    print("Humaira")
    return jsonify({'success': True, 'message': 'Welcome to crop recommendation system'})

@app.route('/predictcrop', methods=['POST'])
def predictCrop():
    try:
        data = request.get_json()

        features = np.array([
            data['N'],
            data['P'],
            data['K'],
            data['rainfall'],
            data['ph'],
            data['humidity'],
            data['temperature']
        ]).reshape(1, -1)  

        prediction = model.predict(features)

        return jsonify({'prediction': {"crop": prediction[0]}})
    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)