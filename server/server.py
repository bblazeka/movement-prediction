from flask import (Flask, request)
from flask_cors import CORS
from . import regression, instance_based, markov
from flask.json import jsonify

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/api/path', methods=['GET', 'POST'])
def path():
    path = request.args.get('input', '')
    user = int(request.args.get('user', ''))
    training, query = regression.prepare_data(path,user=user)
    horizontal, vertical = regression.poly_regression(training)
    formatted = regression.formatting(horizontal,vertical,training,query)
    formatted["instancebased"] = instance_based.formatting(instance_based.get_similar(path))
    return jsonify(formatted)

@app.route('/api/ibl', methods=['GET', 'POST'])
def ibl():
    path = request.args.get('input', '')
    return jsonify(instance_based.get_similar(path))

@app.route('/api/markov', methods=['GET', 'POST'])
def markovModel():
    path = request.args.get('input', '')
    return jsonify(markov.predict("4610600"))