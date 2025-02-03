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

load_dotenv()

model = joblib.load('./modules/crop_recommendation_model.pkl')

app = Flask(__name__)

bcrypt.init_app(app)

#Database Configuration:
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

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

# Register blueprints (user-auth route)
app.register_blueprint(auth_bp)


@app.route('/', methods=['GET'])
def welcome():
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
    app.run(debug=True)