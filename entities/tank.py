import math
import pygame

import entities
import entities.projectile
import playfield
import images
from vector import Vector

class Tank(entities.Entity, entities.ProjectileCollider, entities.Blocking):
    heading = Vector(0, -1)
    move = False
    hitpoints = 10
    movementSpeed = 1

    imageNorth = None
    imageEast = None
    imageSouth = None
    imageWest = None

    def __init__(self, location, heading = Vector(1, 0)):
        self.imageNorth = images.get('tank_north')
        self.imageEast = images.get('tank_east')
        self.imageSouth = images.get('tank_south')
        self.imageWest = images.get('tank_west')

        self.setLocation(location)
        self.setHeading(heading)

    def update(self, time, timePassed):
        if self.move:
            movementVector = self.heading.multiplyScalar(self.movementSpeed * timePassed * 0.2)
            self.setLocation(self.location.add(movementVector))
            
            if movementVector.x < 0:
                self.handleLeftCollisions()
            elif movementVector.x > 0:
                self.handleRightCollisions()
            elif movementVector.y < 0:
                self.handleTopCollisions()
            elif movementVector.y > 0:
                self.handleBottomCollisions()

        self.move = False
        pass

    def handleLeftCollisions(self):
        collision = self.checkVerticalCollisions(self.boundingRectangle.left)
        if not collision is None:
            self.setLocation(Vector(collision.location[0] + collision.size[0], self.location.y))

    def handleRightCollisions(self):
        collision = self.checkVerticalCollisions(self.boundingRectangle.right - 1)
        if not collision is None:
            self.setLocation(Vector(collision.location[0] - self.size.x, self.location.y))

    def handleTopCollisions(self):
        collision = self.checkHorizontalCollisions(self.boundingRectangle.top)
        if not collision is None:
            self.setLocation(Vector(self.location.x, collision.location[1] + collision.size[1]))

    def handleBottomCollisions(self):
        collision = self.checkHorizontalCollisions(self.boundingRectangle.bottom - 1)
        if not collision is None:
            self.setLocation(Vector(self.location.x, collision.location[1] - self.size.y))

    def checkVerticalCollisions(self, x):
        start = Vector(x, self.boundingRectangle.top)
        end = start.add(Vector(0, self.size.y - 1))
        increment = Vector(0, playfield.blockSize)

        return self.checkLineCollisions(start, end, increment)

    def checkHorizontalCollisions(self, y):
        start = Vector(self.boundingRectangle.left, y)
        end = start.add(Vector(self.size.x - 1, 0))
        increment = Vector(playfield.blockSize, 0)

        return self.checkLineCollisions(start, end, increment)

    def checkLineCollisions(self, start, end, increment):
        collision = self.checkLineTileCollisions(start, end, increment)
        if not collision == None:
            return collision
        else:
            return self.checkLineEntityCollisions(start, end)

    def checkLineTileCollisions(self, start, end, increment):
        steps = int(math.ceil(self.size.y / playfield.blockSize)) + 1
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
        collidingEntities = entities.manager.findEntitiesInRectangle(area, exceptEntity=self, typeFilter=entities.Blocking)
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
        self.setHeading(vector)
        self.move = True

    def fire(self):
        projectile = entities.projectile.Projectile(self.location, self.heading.toUnit(), self)
        entities.manager.add(projectile)

    def hitByProjectile(self, projectile):
        self.hitpoints -= projectile.power
        if self.hitpoints <= 0:
            self.destroy()

    def setImage(self, image):
        self.image = image
        self.setSize(Vector(self.image.get_width(), self.image.get_height()))

    def setHeading(self, newHeading):
        self.heading = newHeading
        self.updateImageBasedOnHeading()

    def updateImageBasedOnHeading(self):
        if self.heading.y < 0:
            self.setImage(self.imageNorth)
        elif self.heading.y > 0:
            self.setImage(self.imageSouth)
        elif self.heading.x < 0:
            self.setImage(self.imageWest)
        elif self.heading.x > 0:
            self.setImage(self.imageEast)

    def destroy(self):
        self.markDisposable()

class Collision:
    def __init__(self, location, size):
        self.location = location
        self.size = size