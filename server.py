from flask import Flask, jsonify, request
from celery import Celery
from tasks import test, get_variable, run_roam
import os
import json
import platform
import subprocess

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest:guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')

ROAM_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'roam.py')
ROAM_CLASSES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'roam_classes.py')
ROAM_CALLS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'roam_calls.py')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to B.R.A.D'})

@app.route('/connection_test', methods=['POST'])
def connection_test():
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

@app.route('/roam', methods=['POST'])
def roam():
    try:
        start_node_name = ''
        start_node_class_name = ''
        node_names = []

        data = request.json

        with open(ROAM_CLASSES_PATH, 'w') as class_writer, open(ROAM_CALLS_PATH, 'w') as call_writer, open(ROAM_PATH, 'w') as roam_writer:
            # class writes
            class_writer.write('import traceback\n')
            class_writer.write('import time\n')
            class_writer.write('\nfrom brad import Brad\n')
            class_writer.write('\ndrone = Brad()\n')
            # call writes
            call_writer.write('from concurrent.futures import ThreadPoolExecutor\n')
            call_writer.write('from roam_classes import *\n\n')
            call_writer.write('def run_calls_in_parallel(calls):\n')
            call_writer.write('    with ThreadPoolExecutor() as executor:\n')
            call_writer.write('        running_calls = [executor.submit(call) for call in calls]\n');
            call_writer.write('        for running_call in running_calls:\n');
            call_writer.write('            running_call.result()\n');
            call_writer.write('# Node instances\n');
            
            nodes = data['nodes']['map_nodes'].values()
            for node in nodes:
                if(len(start_node_name) == 0):
                    start_node_name = node['name']
                    start_node_class_name = node['class_name']
                node_names.append(node['name'])
                class_writer.write(node['class_code'])
                class_writer.write('\n\n')
                call_writer.write(f"{node['name']} = {node['class_name']}()\n")
                for var_name, var_value in node['variable_json'].items():
                    call_writer.write(f"{node['name']}.__setattr__(\"{var_name}\", {var_value})\n")
            call_writer.write('\n')

            # Write the node call functions
            for node in nodes:
                call_writer.write(node['call_code'])
                # Attach the call function to the node object run method
                call_writer.write(f"\n{node['name']}.setRunCall({node['name']}_call)\n\n")
            
            # Create roam.py
            roam_writer.write('import json\n')
            roam_writer.write('import sys\n\n')
            roam_writer.write('from logger import Logger\n')
            roam_writer.write('from roam_calls import *\n\n\n')
            roam_writer.write('rout = Logger()\n')
            roam_writer.write('\ndef main(feed=None):\n')
            roam_writer.write('    try:\n')
            roam_writer.write('        if feed:\n')
            roam_writer.write('            feed = json.load(feed)\n')
            roam_writer.write('        else:\n')
            roam_writer.write("            feed = {'test': 'This is test data!'}\n")
            roam_writer.write(f"        {start_node_name}.run(inputs=feed, logger=rout)\n\n")
            roam_writer.write('    except Exception:\n')
            roam_writer.write('        print(traceback.format_exc())\n')
            roam_writer.write('    rout.show()\n')
            roam_writer.write('    rout.writeToFile()\n')
            roam_writer.write('    sys.stdout.flush()\n')
            roam_writer.write("\n\nif __name__ == '__main__':\n")
            roam_writer.write('    main() # main(sys.stdin) w/ cat feed.json | python3 roam.py\n')
            roam_writer.write('    drone.endThreads()')

        run_roam.apply_async(args=[ROAM_PATH])
        #test_data = run_roam(ROAM_PATH)
            
        return jsonify({'data': 'ROAM running...'})
    except Exception as error:
        return jsonify({'error': str(error)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)