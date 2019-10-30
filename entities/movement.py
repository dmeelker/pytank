import math
import pygame

import playfield
import entities
from utilities import Vector

class Collision:
    def __init__(self, location, size, collidedObject):
        self.location = location
        self.size = size
        self.collidedObject = collidedObject

class MovementHandler:
    def __init__(self, entity, tileBlockFunction, entityIgnoreFunction = None):
        self.entity = entity
        self.tileBlockFunction = tileBlockFunction
        self.entityIgnoreFunction = entityIgnoreFunction

    def moveEntity(self, movementVector):
        collisions = []

        def addIfNotNone(collision):
            if not collision is None:
                collisions.append(collision)

        if movementVector.x != 0:
            self.entity.move(Vector(movementVector.x, 0))
            if movementVector.x < 0:
                addIfNotNone(self.handleLeftCollisions())
            elif movementVector.x > 0:
                addIfNotNone(self.handleRightCollisions())

        if movementVector.y != 0:
            self.entity.move(Vector(0, movementVector.y))
            if movementVector.y < 0:
                addIfNotNone(self.handleTopCollisions())
            elif movementVector.y > 0:
                addIfNotNone(self.handleBottomCollisions())
        
        return collisions

    def canMove(self, movementVector):
        if movementVector.x != 0:
            if movementVector.x < 0:
                if not self.checkLeftCollisions() is None:
                    return False
            elif movementVector.x > 0:
                if not self.checkRightCollisions() is None:
                    return False

        if movementVector.y != 0:
            if movementVector.y < 0:
                if not self.checkTopCollisions() is None:
                    return False
            elif movementVector.y > 0:
                if not self.checkBottomCollisions() is None:
                    return False
        return True

    def handleLeftCollisions(self):
        collision = self.checkLeftCollisions()
        if not collision is None:
            self.entity.setLocation(Vector(collision.location[0] + collision.size[0], self.entity.location.y))
            return collision
        else:
            return None

    def checkLeftCollisions(self):
        return self.checkVerticalCollisions(self.entity.boundingRectangle.left - 1)

    def handleRightCollisions(self):
        collision = self.checkRightCollisions()
        if not collision is None:
            self.entity.setLocation(Vector(collision.location[0] - self.entity.size.x, self.entity.location.y))
            return collision
        else:
            return None

    def checkRightCollisions(self):
        return self.checkVerticalCollisions(self.entity.boundingRectangle.right)

    def handleTopCollisions(self):
        collision = self.checkTopCollisions()
        if not collision is None:
            self.entity.setLocation(Vector(self.entity.location.x, collision.location[1] + collision.size[1]))
            return collision
        else:
            return None

    def checkTopCollisions(self):
        return self.checkHorizontalCollisions(self.entity.boundingRectangle.top - 1)

    def handleBottomCollisions(self):
        collision = self.checkBottomCollisions()
        if not collision is None:
            self.entity.setLocation(Vector(self.entity.location.x, collision.location[1] - self.entity.size.y))
            return collision
        else:
            return None
    
    def checkBottomCollisions(self):
        return self.checkHorizontalCollisions(self.entity.boundingRectangle.bottom)

    def checkVerticalCollisions(self, x):
        start = Vector(x, self.entity.boundingRectangle.top)
        end = start.add(Vector(0, self.entity.size.y - 1))
        increment = Vector(0, playfield.blockSize)

        return self.checkLineCollisions(start, end, increment)

    def checkHorizontalCollisions(self, y):
        start = Vector(self.entity.boundingRectangle.left, y)
        end = start.add(Vector(self.entity.size.x - 1, 0))
        increment = Vector(playfield.blockSize, 0)

        return self.checkLineCollisions(start, end, increment)

    def checkLineCollisions(self, start, end, increment):
        collision = self.checkLineTileCollisions(start, end, increment)
        if not collision == None:
            return collision
        else:
            return self.checkLineEntityCollisions(start, end)

    def checkLineTileCollisions(self, start, end, increment):
        steps = int(math.ceil(self.entity.size.y / playfield.blockSize)) + 1
        location = start

        for _ in range(steps):
            collision = self.checkTileCollisions(location)
            if not collision is None:
                return collision
            else:
                location = location.add(increment)
                location.y = min(location.y, end.y)
                location.x = min(location.x, end.x)

    def checkLineEntityCollisions(self, start, end):
        area = pygame.Rect(start.x, start.y, max(end.x - start.x, 1), max(end.y - start.y, 1))
        collidingEntities = entities.manager.findEntitiesInRectangle(area, exceptEntity=self.entity, typeFilter=entities.Blocking)

        for entity in collidingEntities:
            if not(self.ignoreEntity(entity)):
                return Collision(entity.location.toIntTuple(), entity.size.toIntTuple(), entity)
        else:
            return None

    def ignoreEntity(self, entity):
        if self.entityIgnoreFunction != None:
            return self.entityIgnoreFunction(entity)
        else:
            return False

    def checkTileCollisions(self, pixelCoordinates):
        tileCoordinates = playfield.convertPixelToTileCoordinates(pixelCoordinates.toIntTuple())
        tilePixelCoordinates = (tileCoordinates[0] * playfield.blockSize, tileCoordinates[1] * playfield.blockSize)

        if not playfield.containsPixelCoordinates(pixelCoordinates.x, pixelCoordinates.y):
            size = (playfield.blockSize, playfield.blockSize)
            return Collision(tilePixelCoordinates, size, None)

        tile = playfield.getTileAtPixel(pixelCoordinates.x, pixelCoordinates.y)

        if self.tileBlockFunction(tile):
            size = (playfield.blockSize, playfield.blockSize)
            return Collision(tilePixelCoordinates, size, tile)
        else:
            return None