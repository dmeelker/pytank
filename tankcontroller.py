import pygame
import random
import utilities
from utilities import Timer

class TankController:
    def update(self, time, timePassed):
        pass

class PlayerTankController(TankController):
    def __init__(self, entity):
        self.entity = entity
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.fire = False
    
    def update(self, time, timePassed):
        if self.moveLeft:
            self.entity.moveInDirection(utilities.vectorLeft)
        elif self.moveRight:
            self.entity.moveInDirection(utilities.vectorRight)
        if self.moveUp:
            self.entity.moveInDirection(utilities.vectorUp)
        elif self.moveDown:
            self.entity.moveInDirection(utilities.vectorDown)
        if self.fire:
            self.entity.fire(time)

class AiTankController(TankController):
    directions = [utilities.vectorUp, utilities.vectorRight, utilities.vectorDown, utilities.vectorLeft]
    
    def __init__(self, entity):
        self.entity = entity
        self.fireTimer = Timer(500)
    
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