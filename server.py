from flask import Flask, jsonify, request
from celery import Celery
from tasks import test, get_variable
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

@app.route('/variable', methods=['POST'])
def variable_route():
    try:
        # Access JSON data from the request body
        data = request.json
        variable_name = data.get('variable_name')

        #get_variable.apply_async(args=[variable_name])
        result = get_variable(variable_name)
        return jsonify({variable_name: str(result)})

    except Exception as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)