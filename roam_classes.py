import traceback
import time

from brad import Brad

drone = Brad()
class Start:
    def __init__(self):
        self.call = None


    def setRunCall(self, call):
        self.call = call

    def run(self, *args, **kwargs):
        rout = kwargs.get('logger')
        try:
            inputs = kwargs.get('inputs')
            if self.call and inputs:
                self.call(inputs, logger=rout)
        except Exception:
            if drone:
                drone.sendLog(f'start Error: {traceback.format_exc()}')
            else:
                print(f'start Error: {traceback.format_exc()}')

class Distance_From_Front:
    def __init__(self):
        self.call = None
        self.intial_delay = None

    def setRunCall(self, call):
        self.call = call

    def run(self, *args, **kwargs):
        rout = kwargs.get('logger')
        try:
            inputs = kwargs.get('inputs')
            if self.call and inputs:
                self.call(inputs, logger=rout)
        except Exception:
            if drone:
                drone.sendLog(f'distance_from_front Error: {traceback.format_exc()}')
            else:
                print(f'distance_from_front Error: {traceback.format_exc()}')

class Capture_Image:
    def __init__(self):
        self.call = None
        self.initial_delay = None

    def setRunCall(self, call):
        self.call = call

    def run(self, *args, **kwargs):
        rout = kwargs.get('logger')
        try:
            inputs = kwargs.get('inputs')
            if self.call and inputs:
                self.call(inputs, logger=rout)
        except Exception:
            if drone:
                drone.sendLog(f'capture_image Error: {traceback.format_exc()}')
            else:
                print(f'capture_image Error: {traceback.format_exc()}')

