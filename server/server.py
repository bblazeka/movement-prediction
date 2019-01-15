from flask import (Flask, request)
from flask_cors import CORS
from . import regression
from flask.json import jsonify

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/api/path/<path>', methods=['GET', 'POST'])
def path(path):
    predict = regression.regress([[-8.585,41.148],[-8.585,41.148],[-8.585,41.148],[-8.585,41.148]],user=int(path))
    return jsonify(predict)