from flask import (Flask, request)
from flask_cors import CORS
from .regression import Regression
from . import instance, markov, base
from flask.json import jsonify

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/api/compare', methods=['GET'])
def compare():
    # regression
    path = request.args.get('input', '')
    user = int(request.args.get('user', ''))
    regression = Regression()
    regression.prepare_data(path,user=user)
    regression.poly_regression()
    regression.formatting()
    # instance based learning
    ibl = instance.Instance()
    ibl.get_similar(path)
    # markov
    hmm = markov.Markov()
    hmm.predict("39671211")
    return jsonify(base.comparison(regression.get_predict(),ibl.get_predict(),hmm.get_predict()))

@app.route('/api/regression', methods=['GET'])
def path():
    path = request.args.get('input', '')
    user = int(request.args.get('user', ''))
    regression = Regression()
    regression.prepare_data(path,user=user)
    regression.poly_regression()
    return jsonify(regression.formatting())

@app.route('/api/ibl', methods=['GET'])
def ibl():
    path = request.args.get('input', '')
    return jsonify(instance.get_similar(path))

@app.route('/api/markov', methods=['GET'])
def markovModel():
    path = request.args.get('input', '')
    return jsonify(markov.predict("4610600"))