from celery import Celery
import os
import subprocess

app = Celery('tasks', broker='pyamqp://guest:guest@localhost//')

@app.task
def test():
    path = os.path.join(os.path.dirname(__file__), 'brad_test.py')
    
    # Using Popen to run the command asynchronously
    process = subprocess.Popen(['sudo', 'python', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Retrieve the output and error messages if needed
    output, error = process.communicate()
    print(f"output: {str(output)}")
    return "GPIO operation completed successfully"

@app.task
def get_variable(variable_name):
    value = ''
    try:
        path = os.path.join(os.path.dirname(__file__), 'brad_variables.py')
        # Use subprocess.Popen or any other method to interact with hardware
        # Example: subprocess.Popen(['python', 'your_script.py', variable_name])
        # ...
        process = subprocess.Popen(['sudo', 'python', path, variable_name], stdout=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        # Check if the command was successful
        if process.returncode == 0:
            value = stdout.strip()
        else:
            # Handle errors if needed
            value = f"Error: {stderr.strip()}"
        print(f'Task completed for {variable_name}')

    except Exception as e:
        value = f'Task failed for {variable_name}: {str(e)}'
    
    print(f'value: {value}')
    return value