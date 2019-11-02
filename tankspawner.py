import random
import entities
import tankcontroller
import utilities
import tankfactory
from utilities import Timer

class TankSpawner:
    def __init__(self, location):
        self.location = location
        self.spawnTimer = Timer(5000)
        self.resetTimer()

    def update(self, time, timepassed):
        if self.spawnTimer.update(time):
            self.spawn()
    
    def spawn(self):
        tank = tankfactory.createTank(0, self.location)
        entities.manager.add(tank)
        self.resetTimer()

    def resetTimer(self):
        self.spawnTimer.setInterval(random.randint(4500, 5500))
        