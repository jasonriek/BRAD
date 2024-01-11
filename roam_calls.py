from concurrent.futures import ThreadPoolExecutor
from roam_classes import *

def run_calls_in_parallel(calls):
    with ThreadPoolExecutor() as executor:
        running_calls = [executor.submit(call) for call in calls]
        for running_call in running_calls:
            running_call.result()
# Node instances
start = Start()
distance_from_front = Distance_From_Front()
distance_from_front.__setattr__("intial_delay", 1000)
capture_image = Capture_Image()
capture_image.__setattr__("initial_delay", 1000)

def start_call(inputs={}, *args, **kwargs):
    outputs = inputs
    rout = kwargs.get('logger')
    try:

        drone.sendLog(f'___RUNNING start...')
        # Write code here
        
        drone.sendLog(f'___start ran successfully')

    except Exception:
        drone.sendLog(f'start Error: {traceback.format_exc()}')
        drone.sendLog(f'(!)___start failed')

    distance_from_front.run(inputs=outputs, logger=rout)

start.setRunCall(start_call)

def distance_from_front_call(inputs={}, *args, **kwargs):
    outputs = inputs
    rout = kwargs.get('logger')
    try:

        drone.sendLog(f'___RUNNING distance_from_front...')
        # Write code here
        drone.sendLog(drone.distanceFromFront() + ' cm')
        drone.sendLog(f'___distance_from_front ran successfully')

    except Exception:
        drone.sendLog(f'distance_from_front Error: {traceback.format_exc()}')
        drone.sendLog(f'(!)___distance_from_front failed')

    capture_image.run(inputs=outputs, logger=rout)

distance_from_front.setRunCall(distance_from_front_call)

def capture_image_call(inputs={}, *args, **kwargs):
    outputs = inputs
    rout = kwargs.get('logger')
    try:

        drone.sendLog(f'___RUNNING capture_image...')
        drone.delay(capture_image.initial_delay)
        drone.captureImage()
        drone.sendLog(f'___capture_image ran successfully')

    except Exception:
        drone.sendLog(f'capture_image Error: {traceback.format_exc()}')
        drone.sendLog(f'(!)___capture_image failed')

    return outputs
capture_image.setRunCall(capture_image_call)

