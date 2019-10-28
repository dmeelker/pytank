import pygame
import vector

class Entity:
    location = vector.Vector(0, 0)
    size = vector.Vector(0, 0)
    boundingRectangle = pygame.Rect(0, 0, 0, 0)
    disposable = False
    disposed = False

    def update(self, time, timePassed):
        pass

    def render(self, screen, offset):
        pass

    def setLocation(self, newLocation):
        self.location = newLocation
        self.boundingRectangle.left = newLocation.x
        self.boundingRectangle.top = newLocation.y

    def setSize(self, newSize):
        self.size = newSize
        self.boundingRectangle.width = newSize.x
        self.boundingRectangle.height = newSize.y

    def markDisposable(self):
        self.disposable = True

    def dispose(self):
        self.disposed = True

class ProjectileCollider:
    def hitByProjectile(self, projectile):
        pass