import entities
import entities.manager
import playfield
import images
import vector

class Projectile(entities.Entity):
    directionVector = vector.Vector(0, 0)
    source = None
    power = 1

    def __init__(self, location, directionVector, source, power = 1):
        self.image = images.get('projectile')
        self.setSize(vector.Vector(self.image.get_width(), self.image.get_height()))
        self.setLocation(location)
        self.directionVector = directionVector
        self.source = source
        self.power = power

    def update(self, time, timePassed):
        self.setLocation(self.location.add(self.directionVector.multiplyScalar(timePassed * 0.25)))
        self.checkEntityCollisions()
        self.checkPlayfieldCollisions()

    def checkEntityCollisions(self):
        collidingEntities = entities.manager.findEntitiesInRectangle(self.boundingRectangle, exceptEntity=self)

        for collidingEntity in collidingEntities:
            if isinstance(collidingEntity, entities.ProjectileCollider) and collidingEntity != self.source:
                collidingEntity.hitByProjectile(self)
                self.markDisposable()
                return

    def checkPlayfieldCollisions(self):
        if not playfield.containsPixelCoordinates(self.location.x + 2, self.location.y + 2):
            self.markDisposable()
            return

        tile = playfield.getTileAtPixel(self.location.x + 2, self.location.y + 2)

        if not tile is None and tile.blocksMovement:
            tile.hitByProjectile(self)
            self.markDisposable()

    def render(self, screen, offset):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))

