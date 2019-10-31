import entities
import entities.manager
import entities.tank
from entities.movement import MovementHandler
import playfield
import images
from utilities import Vector

class Projectile(entities.Entity, entities.ProjectileCollider):
    def __init__(self, location, directionVector, source, power = 1):
        super().__init__()
        self.image = images.get('projectile')
        self.setSize(Vector(self.image.get_width(), self.image.get_height()))
        self.setLocation(location)
        self.directionVector = directionVector
        self.source = source
        self.power = power

        tileBlockedFunction = lambda tile: not tile is None and tile.blocksProjectiles
        self.movementHandler = MovementHandler(self, tileBlockedFunction, entityIgnoreFunction=lambda entity: self.collisionIgnoreFunction(entity))

    def update(self, time, timePassed):
        movementVector = self.directionVector.multiplyScalar(timePassed * 0.25)
        collisions = self.movementHandler.moveEntity(movementVector)
        self.handleCollisions(collisions, time)

    def handleCollisions(self, collisions, time):
        if len(collisions) > 0:
            collision = collisions[0]
            if collision.collidedObject is None:
                self.markDisposable()
            elif isinstance(collision.collidedObject, playfield.Tile):
                collision.collidedObject.hitByProjectile(self, time)
                self.markDisposable()
            elif isinstance(collision.collidedObject, entities.ProjectileCollider):
                collision.collidedObject.hitByProjectile(self, time)
                self.markDisposable()
                return

    def collisionIgnoreFunction(self, entity):
        if isinstance(entity, entities.tank.Tank):
            return self.shouldIgnoreTank(entity)
        elif entity == self.source:
            return True
        
        return False

    def shouldIgnoreTank(self, tank):
        return self.source.playerControlled == tank.playerControlled

    def hitByProjectile(self, projectile, time):
        self.markDisposable()

    def render(self, screen, offset, time):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))
