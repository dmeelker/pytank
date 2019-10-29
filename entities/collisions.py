import math
import pygame

import playfield
import entities
from vector import Vector

class CollisionHandler:
    def __init__(self, entity):
        self.entity = entity

    def handleLeftCollisions(self):
        collision = self.checkVerticalCollisions(self.entity.boundingRectangle.left)
        if not collision is None:
            self.entity.setLocation(Vector(collision.location[0] + collision.size[0], self.entity.location.y))

    def handleRightCollisions(self):
        collision = self.checkVerticalCollisions(self.entity.boundingRectangle.right - 1)
        if not collision is None:
            self.entity.setLocation(Vector(collision.location[0] - self.entity.size.x, self.entity.location.y))

    def handleTopCollisions(self):
        collision = self.checkHorizontalCollisions(self.entity.boundingRectangle.top)
        if not collision is None:
            self.entity.setLocation(Vector(self.entity.location.x, collision.location[1] + collision.size[1]))

    def handleBottomCollisions(self):
        collision = self.checkHorizontalCollisions(self.entity.boundingRectangle.bottom - 1)
        if not collision is None:
            self.entity.setLocation(Vector(self.entity.location.x, collision.location[1] - self.entity.size.y))

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
        entity = next(collidingEntities, None)
        if not entity == None:
            return Collision(entity.location.toIntTuple(), entity.size.toIntTuple())
        else:
            return None

    def checkTileCollisions(self, pixelCoordinates):
        if self.pixelBlocked(pixelCoordinates):
            tileCoordinates = playfield.convertPixelToTileCoordinates(pixelCoordinates.toIntTuple())
            tilePixelCoordinates = (tileCoordinates[0] * playfield.blockSize, tileCoordinates[1] * playfield.blockSize)
            size = (playfield.blockSize, playfield.blockSize)
            return Collision(tilePixelCoordinates, size)
        else:
            return None

    def pixelBlocked(self, coordinates):
        tile = playfield.getTileAtPixel(coordinates.x, coordinates.y)
        return not tile is None and tile.blocksMovement

class Collision:
    def __init__(self, location, size):
        self.location = location
        self.size = size