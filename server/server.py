from flask import (Flask, request)
from flask_cors import CORS
from . import regression
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
    predict = regression.regress(path,user=user)
    return jsonify(predict)