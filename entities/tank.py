import math
import pygame

import entities
import entities.projectile
import playfield
import images
from vector import *

class Tank(entities.Entity, entities.ProjectileCollider, entities.Blocking):
    aimVector = Vector(0, -1)
    move = False
    hitpoints = 10
    movementSpeed = 1

    def __init__(self, location, aimVector = Vector(1, 0)):
        self.image = images.get('concrete')
        self.setSize(Vector(self.image.get_width(), self.image.get_height()))
        self.setLocation(location)
        self.aimVector = aimVector

    def update(self, time, timePassed):
        if self.move:
            self.setLocation(self.location.add(self.aimVector.multiplyScalar(self.movementSpeed * timePassed * 0.2)))
            
            if self.aimVector.x < 0:
                self.checkLeftCollisions()
            elif self.aimVector.x > 0:
                self.checkRightCollisions()
            elif self.aimVector.y < 0:
                self.checkTopCollisions()
            elif self.aimVector.y > 0:
                self.checkBottomCollisions()

        self.move = False
        pass

    def checkLeftCollisions(self):
        moveBackFunction = lambda coordinates, size: Vector(coordinates[0] + size[0], self.location.y)
        self.checkVerticalCollisions(self.boundingRectangle.left, moveBackFunction)

    def checkRightCollisions(self):
        moveBackFunction = lambda coordinates, size: Vector(coordinates[0] - self.size.x, self.location.y)
        self.checkVerticalCollisions(self.boundingRectangle.right - 1, moveBackFunction)

    def checkTopCollisions(self):
        moveBackFunction = lambda coordinates, size: Vector(self.location.x, coordinates[1] + size[1])
        self.checkHorizontalCollisions(self.boundingRectangle.top, moveBackFunction)

    def checkBottomCollisions(self):
        moveBackFunction = lambda coordinates, size: Vector(self.location.x, coordinates[1] - self.size.y)
        self.checkHorizontalCollisions(self.boundingRectangle.bottom - 1, moveBackFunction)

    def checkVerticalCollisions(self, x, moveBackFunction):
        start = Vector(x, self.boundingRectangle.top)
        end = start.add(Vector(0, self.size.y - 1))
        increment = Vector(0, playfield.blockSize)

        self.checkLineTileCollisions(start, end, increment, moveBackFunction)
        self.checkLineEntityCollisions(start, end, moveBackFunction)

    def checkHorizontalCollisions(self, y, moveBackFunction):
        start = Vector(self.boundingRectangle.left, y)
        end = start.add(Vector(self.size.x - 1, 0))
        increment = Vector(playfield.blockSize, 0)

        self.checkLineTileCollisions(start, end, increment, moveBackFunction)
        self.checkLineEntityCollisions(start, end, moveBackFunction)

    def checkLineTileCollisions(self, start, end, increment, moveBackFunction):
        steps = int(math.ceil(self.size.y / playfield.blockSize)) + 1
        location = start

        for _ in range(steps):
            if self.checkTileCollisions(location, moveBackFunction):
                return
            else:
                location = location.add(increment)
                location.y = min(location.y, end.y)
                location.x = min(location.x, end.x)

    def checkLineEntityCollisions(self, start, end, moveBackFunction):
        area = pygame.Rect(start.x, start.y, max(end.x - start.x, 1), max(end.y - start.y, 1))
        collidingEntities = entities.manager.findEntitiesInRectangle(area, exceptEntity=self, typeFilter=entities.Blocking)
        entity = next(collidingEntities, None)
        if not entity == None:
            self.setLocation(moveBackFunction(entity.location.toIntTuple(), entity.size.toIntTuple()))
            return

    def checkTileCollisions(self, pixelCoordinates, moveBackFunction):
        if self.pixelBlocked(pixelCoordinates):
            tileCoordinates = playfield.convertPixelToTileCoordinates(pixelCoordinates.toIntTuple())
            tilePixelCoordinates = (tileCoordinates[0] * playfield.blockSize, tileCoordinates[1] * playfield.blockSize)
            size = (playfield.blockSize, playfield.blockSize)
            self.setLocation(moveBackFunction(tilePixelCoordinates, size))
            return True
        else:
            return False

    def pixelBlocked(self, coordinates):
        tile = playfield.getTileAtPixel(coordinates.x, coordinates.y)
        return not tile is None and tile.blocksMovement

    def render(self, screen, offset):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))

    def moveLeft(self):
        self.moveToVector(Vector(-1, 0))

    def moveRight(self):
        self.moveToVector(Vector(1, 0))

    def moveUp(self):
        self.moveToVector(Vector(0, -1))

    def moveDown(self):
        self.moveToVector(Vector(0, 1))

    def moveToVector(self, vector):
        self.aimVector = vector
        self.move = True

    def fire(self):
        projectile = entities.projectile.Projectile(self.location, self.aimVector.toUnit(), self)
        entities.manager.add(projectile)

    def hitByProjectile(self, projectile):
        self.hitpoints -= projectile.power
        if self.hitpoints <= 0:
            self.destroy()

    def destroy(self):
        self.markDisposable()

class Collision:
    def __init__(self, location, size):
        self.location = location
        self.size = size