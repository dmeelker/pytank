import entities
import images
from vector import Vector

class Base(entities.Entity, entities.ProjectileCollider, entities.Blocking):
    hitpoints = 10

    def __init__(self, location):
        self.image = images.get('base')
        self.setSize(Vector(self.image.get_width(), self.image.get_height()))
        self.setLocation(location)

    def update(self, time, timePassed):
        pass

    def render(self, screen, offset):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))

    def hitByProjectile(self, projectile):
        self.hitpoints -= projectile.power

        if self.hitpoints <= 0:
            self.markDisposable()
