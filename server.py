from flask import Flask, jsonify, request
from celery import Celery
from tasks import test
import os
import json
import platform
import subprocess

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest:guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to B.R.A.D'})

@app.route('/connection_test', methods=['POST'])
def connection_test():
    test.apply_async()
    return f"Successfully connected to B.R.A.D"

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=3000)