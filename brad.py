import requests
import json
import os
import time
import base64
from datetime import datetime
from PIL import Image
from picamera2 import Picamera2

from logger import Logger
from controls import Controls
from libs.ultrasonic import Ultrasonic

ROAM_SERVER = 'http://192.168.0.13/'

def resize_image(image_path, output_path, new_size=(250, 250)):
    try:
        with Image.open(image_path) as img:
            resized_img = img.resize(new_size)
            resized_img.save(output_path, format='JPEG')
    except Exception as e:
        print(f"Error resizing image: {str(e)}")

FORWARD = 'F'
BACKWARD = 'B'
RIGHT = 'R'
LEFT = 'L'

class Brad:
    def __init__(self):
        self.logger = Logger()
        self.controls = Controls()
        self.controls.thread_condition.start()
        self.ultrasonic = Ultrasonic()

        self.variables = {
            'front_distance': self.distanceFromFront,
            'rear_distance': self.unknownValue,
            'speed': self.speed
        }

    def sendLog(self, message=''):
        try:
            payload = {
                'message': message
            }
            headers = {'content-type': 'application/json'}
            rsp = requests.post(ROAM_SERVER + 'message', 
                                headers=headers, 
                                data=json.dumps(payload))
            self.logger.log(str(rsp.text))
        except Exception as error:
            self.logger.log(str(error))
    
    def delay(self, ms):
        time.sleep(0.001 * ms)
    
    def runUntilTimeout(self, function, seconds, *args, **kwargs):
        function(**kwargs)
        time.sleep(seconds)
        self.controls.order = ['','','','','','']

    def move(self, data):
        self.controls.order = data
        
    def moveForward(self, speed):
        self.move(['CMD_MOVE', '1', '0', '30', str(speed), '0'])
    
    def moveBackward(self, speed):
        self.move(['CMD_MOVE', '1', '0', '-30', str(speed), '0'])
    
    def moveLeft(self, speed):
        self.move(['CMD_MOVE', '1', '-30', '-2', str(speed), '0'])
    
    def moveRight(self, speed):
        self.move(['CMD_MOVE', '1', '30', '1', str(speed), '0'])

    def turnLeft(self, speed):
        self.move(['CMD_MOVE', '2', '-30', '-2', str(speed), '0'])

    def turnRight(self, speed):
        self.move(['CMD_MOVE', '2', '30', '1', str(speed), '0'])

    def captureImage(self):
        picam2 = None
        try:
            filename = f'image_{datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}.jpg'
            path = os.path.join(os.path.dirname(__file__), 'images', filename)
            picam2 = Picamera2()
            picam2.start_and_capture_file(path, delay=1, show_preview=False)
            time.sleep(3)
            resize_image(path, path)
            time.sleep(1)
            # Convert image to base64 for inclusion in JSON
            with open(path, 'rb') as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            self.sendLog('Image taken and saved...')

            # Create JSON payload
            json_payload = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'image': base64_image
            }
            rsp = requests.post(ROAM_SERVER + 'image', json=json_payload)
            self.logger.log(str(rsp.text))
            
        except Exception as error:
            self.sendLog(f'Error {str(error)}')
        finally:
            if picam2:
                picam2.close()  # Close or release the camera resources

    def getVariable(self, variable_name: None, end_threads=False):
        variable = None
        # Check if a command-line argument is provided

        if variable_name:
            variable_method = self.variables.get(variable_name)
            variable = variable_method()
        
        if(end_threads):
            self.endThreads()
        
        return variable
    
    def unknownValue(self):
        return 'Unknown'

    def distanceFromFront(self):
        return str(self.ultrasonic.getDistance())
    
    def speed(self):
        return self.controls.speed()

    def endThreads(self):
        self.controls.running = False
        self.controls.thread_condition.join()
        