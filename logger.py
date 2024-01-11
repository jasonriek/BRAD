from datetime import datetime

class Logger():
    def __init__(self, logger_name=None, to_memory=False):
        self._logs = []
        self.logger_name = logger_name
        self.to_memory = to_memory

    def log(self, string:str, *args, **kwargs):
        string = str(string)
        path = kwargs.get('path')
        if len(args) > 0:
            string += (' ' + ' '.join([str(string_part) for string_part in args]))
        if(self.to_memory):
            self._logs.append(string)
        else:
            self.appendToFile(string, path)
            
    def getLogsFromMemory(self):
        return self._logs
    
    def createLogName(self, path:str=''):
        log_name = f'log_{datetime.now().strftime("%m_%d_%Y")}.txt'
        if self.logger_name:
            log_name = f'{self.logger_name}_{log_name}'
        if path:
            log_name = path
        return log_name
    
    def appendToFile(self, string:str, path:str=''):
        log_name = self.createLogName(path)
        with open(log_name, 'a') as f:
            f.write(f"{string}\n")
    
    def writeToFile(self, path:str=''):
        try:
            log_name = self.createLogName(path)
            with open(log_name, 'a') as f:
                f.write(f"\n\nNEW RUN at: {str(datetime.now())}\n")
                f.write('\n'.join(self._logs))

        except Exception as error:
            print(f'rout Error: {str(error)}')

    def clear(self):
        self._logs.clear()
        
    def show(self):
        print('\n'.join(self._logs))
