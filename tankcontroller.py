import random
import utilities
from utilities import Timer

class TankController:
    directions = [utilities.vectorUp, utilities.vectorRight, utilities.vectorDown, utilities.vectorLeft]
    fireTimer = Timer(500)

    def __init__(self, entity):
        self.entity = entity
    
    def update(self, time, timePassed):
        if self.entity.canMoveInDirection(self.entity.heading):
            self.entity.moveInDirection(self.entity.heading)
        else:
            self.entity.moveInDirection(self.randomDirection())

        if self.fireTimer.update(time):
            self.fire(time)

    def fire(self, time):
        self.entity.fire(time)
        self.pickRandomFireTime()

    def pickRandomFireTime(self):
        self.fireTimer.setInterval(random.randint(400, 600))

    def randomDirection(self):
        return self.directions[random.randint(0, len(self.directions) - 1)]