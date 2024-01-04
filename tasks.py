from celery import Celery
import os
import subprocess

app = Celery('tasks', broker='pyamqp://guest:guest@localhost//')

@app.task
def test():
    path = os.path.join(os.path.dirname(__file__), 'brad_test.py')
    
    # Using Popen to run the command asynchronously
    process = subprocess.Popen(['sudo', 'python', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # You can optionally wait for the process to complete or perform other tasks
    process.wait()

    # Retrieve the output and error messages if needed
    output, error = process.communicate()
    print(f"output: {str(output)}")
    return "GPIO operation completed successfully"