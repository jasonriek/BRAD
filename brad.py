from controls import Controls
from libs.ultrasonic import Ultrasonic

class Brad:
    def __init__(self):
        self.controls = Controls()
        self.ultrasonic = Ultrasonic()

        self.variables = {
            'front_distance': self.getDistanceFromFront,
            'rear_distance': self.unknownValue,
            'speed': self.getSpeed
        }

    def getVariable(self, variable_name: None):
        variable = None
        # Check if a command-line argument is provided

        if variable_name:
            variable_method = self.variables.get(variable_name)
            variable = variable_method()
        
        return variable
    
    def unknownValue(self):
        return 'Unknown'

    def getDistanceFromFront(self):
        return self.ultrasonic.getDistance()
    
    def getSpeed(self):
        return self.controls.speed()
        