import entities
import entities.manager
from entities.movement import MovementHandler
import playfield
import images
import vector


class Projectile(entities.Entity):
    directionVector = vector.Vector(0, 0)
    source = None
    movementHandler = None
    power = 1

    def __init__(self, location, directionVector, source, power = 1):
        self.image = images.get('projectile')
        self.setSize(vector.Vector(self.image.get_width(), self.image.get_height()))
        self.setLocation(location)
        self.directionVector = directionVector
        self.source = source
        self.power = power
        self.movementHandler = MovementHandler(self)

    def update(self, time, timePassed):
        movementVector = self.directionVector.multiplyScalar(timePassed * 0.25)
        collisions = self.movementHandler.moveEntity(movementVector)
        self.handleCollisions(collisions)

    def handleCollisions(self, collisions):
        if len(collisions) > 0:
            collision = collisions[0]
            if isinstance(collision.collidedObject, playfield.Tile):
                collision.collidedObject.hitByProjectile(self)
                self.markDisposable()
            elif isinstance(collision.collidedObject, entities.ProjectileCollider) and collision.collidedObject != self.source:
                collision.collidedObject.hitByProjectile(self)
                self.markDisposable()
                return

    def render(self, screen, offset):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))
