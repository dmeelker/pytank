listenerFunctions = []

def send(message):
    for listenerFunction in listenerFunctions:
        listenerFunction(message)

def register(listenerFunction):
    listenerFunctions.append(listenerFunction)

class TankDestroyedMessage:
    def __init__(self, tank):
        self.tank = tank