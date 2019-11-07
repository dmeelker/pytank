import pygame
from utilities import Vector

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
        pass

    def getLocation(self):
        return self.location

    def setLocation(self, newLocation):
        self.location = newLocation
        self.updateBoundingRectangle()

    def getCenterLocation(self):
        return self.location.add(self.size.multiplyScalar(0.5))

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

class ProjectileCollider:
    def hitByProjectile(self, projectile, time):
        pass

class Blocking:
    pass