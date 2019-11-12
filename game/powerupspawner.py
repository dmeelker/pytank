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
            powerup.setLocation(Vector(location[0] * playfield.blockSize, location[1] * playfield.blockSize))
            return powerup

    def createRandomPowerup(self):
        types = [PowerBoostPowerup, RepairTankPowerup, RepairBasePowerup, DestroyAllTanksPowerup, ShieldPowerup]
        powerupType = types[random.randint(0, len(types) - 1)]
        return powerupType()

    def getRandomPowerupLocation(self):
        availableLocations = self.getAvailableLocations()
        if len(availableLocations) == 0:
            return None
        else:
            randomIndex = random.randint(0, len(availableLocations) - 1)
            return availableLocations[randomIndex]

    def getAvailableLocations(self):
        locations = []
        for y in range(playfield.height - 1):
            for x in range(playfield.width - 1):
                tiles = playfield.getTilesInQuad(x, y)
                for tile in tiles:
                    if tile != None and tile.blocksMovement:
                        break
                else:
                    locations.append((x, y))
        
        return locations
