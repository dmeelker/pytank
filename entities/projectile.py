import entities
import entities.manager
import images
import vector

class Projectile(entities.Entity):
    directionVector = vector.Vector(0, 0)

    def __init__(self, location, directionVector):
        self.image = images.get('projectile')
        self.setSize(vector.Vector(self.image.get_width(), self.image.get_height()))
        self.setLocation(location)
        self.directionVector = directionVector

    def update(self, time, timePassed):
        self.setLocation(self.location.add(self.directionVector.multiplyScalar(timePassed * 0.25)))
        self.checkCollisions()

    def checkCollisions(self):
        collidingEntities = entities.manager.findEntitiesInRectangle(self.boundingRectangle, exceptEntity=self)

        for collidingEntity in collidingEntities:
            if collidingEntity is entities.ProjectileCollider:
                collidingEntity.hitByProjectile(self)
                self.markDisposable()
                return

    def render(self, screen, offset):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))

