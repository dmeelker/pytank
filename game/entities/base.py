import entities
import images
from utilities import Vector

class Base(entities.Entity, entities.ProjectileCollider, entities.Blocking):
    def __init__(self, location):
        super().__init__()
        self.image = images.get('base')
        self.setSize(Vector(self.image.get_width(), self.image.get_height()))
        self.setLocation(location)
        self.hitpoints = 10

    def update(self, time, timePassed):
        pass

    def render(self, screen, offset, time):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))

    def hitByProjectile(self, projectile, time):
        self.hitpoints -= projectile.power

        if self.hitpoints <= 0:
            self.markDisposable()

    def repair(self):
        self.hitpoints = 10

    def getHitpoints(self):
        return self.hitpoints
