from flask import Flask, request, jsonify
import joblib
import numpy as np

model = joblib.load('./modules/crop_recommendation_model.pkl')

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
    