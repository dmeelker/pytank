import pygame
import enum

from utilities import Vector

class Direction(enum.Enum):
    NORTH = 1,
    EAST = 2,
    SOUTH = 3,
    WEST = 4

class Entity:
    def __init__(self):
        self.location = Vector(0, 0)
        self.size = Vector(0, 0)
        self.boundingRectangle = pygame.Rect(0, 0, 0, 0)
        self.disposable = False
        self.disposed = False

    def update(self, time, timePassed):
        pass

    def render(self, screen, offset, time):
        screen.blit(self.image, (int(offset[0] + self.location.x), int(offset[1] + self.location.y)))

    def getLocation(self):
        return self.location

    def setLocation(self, newLocation):
        self.location = newLocation
        self.updateBoundingRectangle()

    def getCenterLocation(self):
        return self.location.add(self.size.multiplyScalar(0.5))

    def centerOn(self, location):
        self.move(location.subtract(self.size.multiplyScalar(0.5)))

    def move(self, movementVector):
        self.setLocation(self.location.add(movementVector))

    def setSize(self, newSize):
        self.size = newSize
        self.updateBoundingRectangle()

    def updateBoundingRectangle(self):
        self.boundingRectangle = pygame.Rect(self.location.x, self.location.y, self.size.x, self.size.y)

    def markDisposable(self):
        self.disposable = True

    def dispose(self):
        self.disposed = True

    def getDirectionFromVector(self, vector):
        if vector.y < 0:
            return Direction.NORTH
        elif vector.y > 0:
            return Direction.SOUTH
        elif vector.x < 0:
            return Direction.WEST
        elif vector.x > 0:
            return Direction.EAST

class ProjectileCollider:
    def hitByProjectile(self, projectile, time):
        pass

class Blocking:
    pass

class Marker(Entity):
    def __init__(self, location):
        super().__init__()
        self.setLocation(location)
        self.setSize(Vector(1, 1))
    def render(self, screen, offset, time):
        screen.set_at((int(offset[0] + self.location.x), int(offset[1] + self.location.y)), pygame.color.Color(255, 255, 255, 255))