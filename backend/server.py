from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    return jsonify({'success': True, 'message': 'Welcome to crop recommendation system'})

if __name__ == '__main__':
    app.run(debug=True)
