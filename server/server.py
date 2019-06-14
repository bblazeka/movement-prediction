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
    mode = request.args.get('mode', '')
    regression.train(path,mode)
    regression.formatting()
    # instance based learning
    ibl = instance.Instance(mode)
    ibl.predict(path)
    # markov
    hmm = markov.Markov(mode)
    hmm.train()
    hmm.predict(path)
    return jsonify(base.comparison(regression.get_predict(),ibl.get_predict(),hmm.get_predict()))

@app.route('/api/evaluate', methods=['GET'])
def evaluate():
    mode = request.args.get('mode', '')
    try:
        radius = int(request.args.get('radius', ''))
    except:
        print('Couldn\'t parse radius')
        radius = 1
    evaluation = eval.Evaluation(mode)
    evals = evaluation.get_evaluations(radius)
    return jsonify(evals)

@app.route('/api/regression', methods=['GET'])
def path():
    path = request.args.get('input', '')
    mode = request.args.get('mode', '')
    regression.train(path,mode)
    regression.formatting()
    return jsonify(regression.formatting())

@app.route('/api/instance', methods=['GET'])
def ibl():
    path = request.args.get('input', '')
    mode = request.args.get('mode', '')
    ibl = instance.Instance(mode)
    ibl.train()
    ibl.predict(path)
    return jsonify(instance.formatting(ibl.get_predict()))

@app.route('/api/markov', methods=['GET'])
def markov_model():
    input = request.args.get('input', '')
    mode = request.args.get('mode', '')
    hmm = markov.Markov(mode)
    hmm.train()
    hmm.predict(input)
    return jsonify(markov.formatting(hmm.get_predict()))

@app.route('/api/tests', methods=['GET'])
def tests():
    mode = request.args.get('mode', '')
    return jsonify(eval.get_geojson_tests(mode))