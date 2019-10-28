import math

import entities
import entities.projectile
import playfield
import images
from vector import *

class Tank(entities.Entity, entities.ProjectileCollider):
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
        moveBackFunction = lambda tileCoordinates: Vector((tileCoordinates[0] + 1) * playfield.blockSize, self.location.y)
        start = Vector(self.boundingRectangle.left, self.boundingRectangle.top)
        end = Vector(start.x, self.boundingRectangle.bottom - 1)
        increment = Vector(0, playfield.blockSize)

        self.checkLinePixelCollisions(start, end, increment, moveBackFunction)

    def checkRightCollisions(self):
        moveBackFunction = lambda tileCoordinates: Vector((tileCoordinates[0] * playfield.blockSize) - self.size.x, self.location.y)
        start = Vector(self.boundingRectangle.right - 1, self.boundingRectangle.top)
        end = Vector(start.x, self.boundingRectangle.bottom - 1)
        increment = Vector(0, playfield.blockSize)

        self.checkLinePixelCollisions(start, end, increment, moveBackFunction)

    def checkTopCollisions(self):
        moveBackFunction = lambda tileCoordinates: Vector(self.location.x, (tileCoordinates[1] + 1) * playfield.blockSize)
        start = Vector(self.boundingRectangle.left, self.boundingRectangle.top)
        end = Vector(self.boundingRectangle.right - 1, start.y)
        increment = Vector(playfield.blockSize, 0)

        self.checkLinePixelCollisions(start, end, increment, moveBackFunction)

    def checkBottomCollisions(self):
        moveBackFunction = lambda tileCoordinates: Vector(self.location.x, (tileCoordinates[1] * playfield.blockSize) - self.size.y)
        start = Vector(self.boundingRectangle.left, self.boundingRectangle.bottom - 1)
        end = Vector(self.boundingRectangle.right - 1, start.y)
        increment = Vector(playfield.blockSize, 0)

        self.checkLinePixelCollisions(start, end, increment, moveBackFunction)

    def checkLinePixelCollisions(self, start, end, increment, moveBackFunction):
        steps = int(math.ceil(self.size.y / playfield.blockSize)) + 1
        location = start

        for _ in range(steps):
            if self.checkTileCollisions(location, moveBackFunction):
                return
            else:
                location = location.add(increment)
                location.y = min(location.y, end.y)
                location.x = min(location.x, end.x)

    def checkTileCollisions(self, pixelCoordinates, moveBackFunction):
        if self.pixelBlocked(pixelCoordinates):
            tileCoordinates = playfield.convertPixelToTileCoordinates(pixelCoordinates.toIntTuple())
            self.setLocation(moveBackFunction(tileCoordinates))
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