import random
import vector

class TankController:
    directions = [vector.up, vector.right, vector.down, vector.left]

    def __init__(self, entity):
        self.entity = entity
    
    def update(self, time, timePassed):
        if self.entity.canMoveInDirection(self.entity.heading):
            self.entity.moveInDirection(self.entity.heading)
        else:
            self.entity.moveInDirection(self.randomDirection())

        pass

    def randomDirection(self):
        return self.directions[random.randint(0, len(self.directions) - 1)]