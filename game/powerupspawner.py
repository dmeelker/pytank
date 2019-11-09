import random

import playfield
import entities.manager
from entities.powerup import *
from utilities import Vector

class PowerupSpawner():
    def spawn(self):
        powerup = self.createRandomPowerupAtRandomLocation()
        if powerup == None:
            return None
        
        entities.manager.add(powerup)
        return powerup

    def createRandomPowerupAtRandomLocation(self):
        location = self.getRandomPowerupLocation()
        if location == None:
            return None
        else:
            powerup = self.createRandomPowerup()
            powerup.setLocation(Vector(location[0], location[1]))
            return powerup

    def createRandomPowerup(self):
        return PowerBoostPowerup()

    def getRandomPowerupLocation(self):
        for i in range(20):
            x = random.randint(0, playfield.width - 1)
            y = random.randint(0, playfield.height - 1)

            tile = playfield.getTile(x, y)
            if tile == None or not tile.blocksMovement:
                return (x, y)
        return None