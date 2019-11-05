import pygame
import random
import playfield
import utilities
from utilities import Timer
import pathfinder
import gamecontroller

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
        self.targetLocation = None
        self.plannedPath = None
        self.pathStepIndex = None
    
    def update(self, time, timePassed):
        if self.targetLocation is None:
            self.plotPathToLocation(gamecontroller.base.location)
        else:
            self.moveTankAlongPath()

        # if self.entity.canMoveInDirection(self.entity.heading):
        #     self.entity.moveInDirection(self.entity.heading)
        # else:
        #     self.entity.moveInDirection(self.randomDirection())

        if self.fireTimer.update(time):
            self.fire(time)

    def fire(self, time):
        self.entity.fire(time)
        self.pickRandomFireTime()

    def pickRandomFireTime(self):
        self.fireTimer.setInterval(random.randint(400, 600))

    def randomDirection(self):
        return self.directions[random.randint(0, len(self.directions) - 1)]

    def plotPathToLocation(self, targetLocation):
        path = self.findPathToLocation(targetLocation)

        if path != None:
            self.targetLocation = targetLocation
            self.plannedPath = path
            self.pathStepIndex = 0

    def moveTankAlongPath(self):
        if self.arrivedAtTarget():
            return

        targetLocation = self.getCurrentTargetLocation()
        self.moveTowardsLocation(targetLocation)
        self.updateCurrentPathIndex()

    def updateCurrentPathIndex(self):
        targetLocation = self.getCurrentTargetLocation()

        if self.locationReached(targetLocation):
            self.pathStepIndex += 1

    def getCurrentTargetLocation(self):
        targetCell = self.plannedPath[self.pathStepIndex + 1]
        return (targetCell[0] * 16, targetCell[1] * 16)

    def moveTowardsLocation(self, targetLocation):
        location = self.entity.location
        if location.x < targetLocation[0]:
            self.entity.moveInDirection(utilities.vectorRight)
        elif location.x > targetLocation[0]:
            self.entity.moveInDirection(utilities.vectorLeft)
        elif location.y < targetLocation[1]:
            self.entity.moveInDirection(utilities.vectorDown)
        elif location.y > targetLocation[1]:
            self.entity.moveInDirection(utilities.vectorUp)

    def locationReached(self, targetLocation):
        location = self.entity.location
        
        if abs(targetLocation[0] - location.x) > 1:
            return False
        elif abs(targetLocation[1] - location.y) > 1:
            return False
        else:
            return True

    def arrivedAtTarget(self):
        return self.locationReached(self.plannedPath[-1])

    

    def findPathToLocation(self, targetLocation):
        searchSpace = self.generateSearchSpace()
        pathFinder = pathfinder.PathFinder(searchSpace)
        return pathFinder.find(self.toSearchSpaceCoordinateTuple(self.entity.location), self.toSearchSpaceCoordinateTuple(targetLocation))

    def toSearchSpaceCoordinateTuple(self, coordinates):
        return (int(coordinates.x / 16), int(coordinates.y / 16))

    def generateSearchSpace(self):
        grid = pathfinder.SearchGrid(int(playfield.width / 2), int(playfield.height / 2))

        for x in range(grid.width):
            for y in range(grid.height):
                grid.set(x, y, self.getSearchSpaceCellValueForTileQuad(x, y))

        return grid

    def getSearchSpaceCellValueForTileQuad(self, searchSpaceX, searchSpaceY):
        tileSpaceX = searchSpaceX * 2
        tileSpaceY = searchSpaceY * 2
        
        return max( \
            self.getSearchSpaceCellValueFromPlayfield(tileSpaceX, tileSpaceY), \
            self.getSearchSpaceCellValueFromPlayfield(tileSpaceX + 1, tileSpaceY), \
            self.getSearchSpaceCellValueFromPlayfield(tileSpaceX, tileSpaceY + 1), \
            self.getSearchSpaceCellValueFromPlayfield(tileSpaceX + 1, tileSpaceY + 1))

    def getSearchSpaceCellValueFromPlayfield(self, x, y):
        tile = playfield.getTile(x, y)
        return self.getSearchSpaceCellValueForTile(tile)

    def getSearchSpaceCellValueForTile(self, tile):
        if tile is None:
            return 0
        elif tile.tileType == playfield.TileType.BRICK:
            return 1
        elif tile.tileType == playfield.TileType.CONCRETE:
            return 100
        elif tile.tileType == playfield.TileType.WATER:
            return 100
        else:
            return 0
        