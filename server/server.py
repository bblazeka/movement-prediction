from flask import (Flask, request)
from flask_cors import CORS
from .regression import Regression
from . import eval, instance, markov, base
from flask.json import jsonify

app = Flask(__name__)
CORS(app)

regression = Regression()

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/api/compare', methods=['GET'])
def compare():
    # regression
    path = request.args.get('input', '')
    user = int(request.args.get('user', ''))
    regression.prepare_sumo_data(path)
    regression.poly_regression()
    regression.formatting()
    # instance based learning
    ibl = instance.Instance()
    ibl.get_similar(path)
    # markov
    hmm = markov.Markov()
    hmm.predict(path)
    return jsonify(base.comparison(regression.get_predict(),ibl.get_predict(),hmm.get_predict()))

@app.route('/api/evaluate', methods=['GET'])
def evaluate():
    path = request.args.get('input', '')
    try:
        radius = int(request.args.get('radius', ''))
    except:
        print('Couldn\'t parse radius')
        radius = 1
    evaluation = eval.Evaluation(path)
    evals = evaluation.get_evaluations(radius)
    return jsonify(evals)

@app.route('/api/regression', methods=['GET'])
def path():
    path = request.args.get('input', '')
    user = int(request.args.get('user', ''))
    regression.prepare_sumo_data(path)
    regression.poly_regression()
    regression.formatting()
    return jsonify(regression.formatting())

@app.route('/api/ibl', methods=['GET'])
def ibl():
    path = request.args.get('input', '')
    return jsonify(instance.get_similar(path))

@app.route('/api/markov', methods=['GET'])
def markov_model():
    path = request.args.get('input', '')
    return jsonify(markov.predict("4610600"))

@app.route('/api/tests', methods=['GET'])
def tests():
    return jsonify(eval.get_geojson_tests())