import sys

from brad import Brad

if __name__ == '__main__':
    brad = Brad()
    variable_name = None
    if len(sys.argv) >= 2:    
        # Get the variable name from the command-line argument
        variable_name = sys.argv[1]
        if variable_name:
            variable_name = variable_name.strip().lower()
        print(brad.getVariable(variable_name, True))