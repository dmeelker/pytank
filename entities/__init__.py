import pygame
from utilities import Vector

class Entity:
    location = Vector(0, 0)
    size = Vector(0, 0)
    boundingRectangle = pygame.Rect(0, 0, 0, 0)
    disposable = False
    disposed = False

    def update(self, time, timePassed):
        pass

    def render(self, screen, offset):
        pass

    def setLocation(self, newLocation):
        self.location = newLocation
        self.updateBoundingRectangle()

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
    def hitByProjectile(self, projectile):
        pass

class Blocking:
    pass