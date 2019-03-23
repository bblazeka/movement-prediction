from flask import (Flask, request)
from flask_cors import CORS
from . import regression
from flask.json import jsonify
from .neural_network import NeuralNetwork

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/api/path', methods=['GET', 'POST'])
def path():
    path = request.args.get('input', '')
    user = int(request.args.get('user', ''))
    points, query = regression.prepare_data(path,user=user)
    horizontal, vertical = regression.poly_regression(points)
    formatted = regression.formatting(horizontal,vertical,points,query)
    return jsonify(formatted)

@app.route('/api/alternative', methods=['GET', 'POST'])
def alternative():
    network = NeuralNetwork()
    return jsonify(network.evaluating())