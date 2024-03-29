import math
import pygame

import entities
import entities.manager
import entities.base
from .movement import MovementHandler
import playfield
import images
from utilities import Vector

class Projectile(entities.Entity, entities.ProjectileCollider):
    def __init__(self, location, directionVector, source, power = 1, breaksConcrete = False):
        super().__init__()
        
        self.direction = self.getDirectionFromVector(directionVector)
        self.image = self.getImageBasedOnDirection()

        self.setSize(Vector(self.image.get_width(), self.image.get_height()))
        self.halfSize = math.ceil(self.size.x / 2)
        self.setLocation(location)
        self.directionVector = directionVector
        self.source = source
        self.power = power
        self.breaksConcrete = breaksConcrete
        self.lastMoveTime = pygame.time.get_ticks()

        tileBlockedFunction = lambda tile: not tile is None and tile.blocksProjectiles
        self.movementHandler = MovementHandler(self, tileBlockedFunction, entityIgnoreFunction=self.collisionIgnoreFunction)

    def getImageBasedOnDirection(self):
        if self.direction == entities.Direction.NORTH:
            return images.get('projectile_north')
        elif self.direction == entities.Direction.EAST:
            return images.get('projectile_east')
        elif self.direction == entities.Direction.SOUTH:
            return images.get('projectile_south')
        elif self.direction == entities.Direction.WEST:
            return images.get('projectile_west')

    def update(self, time, timePassed):
        movementSteps = int((time - self.lastMoveTime ) / 20)
        if movementSteps > 0:
            movementVector = self.directionVector.multiplyScalar(5)
            for _ in range(movementSteps):
                collisions = self.movementHandler.moveEntity(movementVector)
                if len(collisions) > 0:
                    self.handleCollisions(collisions, time)
                    break
            self.lastMoveTime = time

    def handleCollisions(self, collisions, time):
        collision = collisions[0]
        if collision.collidedObject is None:
            self.markDisposable()
        elif self.isCollidableObject(collision.collidedObject):
            self.explode(time)

    def explode(self, time):
        range = 3
        centerLocation = self.getCenterLocation().add(self.directionVector.multiplyScalar(self.halfSize))
        area = pygame.Rect(centerLocation.x - range, centerLocation.y - range, range*2, range*2)
        #entities.manager.add(entities.Marker(centerLocation))

        self.explodeTiles(area, time)
        self.explodeEntities(area, time)

        self.markDisposable()

    def explodeTiles(self, area, time):
        collidingTiles = playfield.getTilesInPixelArea(area.left, area.top, area.width, area.height)

        for tile in collidingTiles:
            if tile != None:
                tile.hitByProjectile(self, time)

    def explodeEntities(self, area, time):
        collidingEntities = entities.manager.findEntitiesInRectangle(area, typeFilter = entities.ProjectileCollider)

        for entity in collidingEntities:
            if not self.collisionIgnoreFunction(entity):
                entity.hitByProjectile(self, time)

    def isCollidableObject(self, collidedObject):
        return isinstance(collidedObject, playfield.Tile) or isinstance(collidedObject, entities.ProjectileCollider)

    def collisionIgnoreFunction(self, entity):
        if isinstance(entity, entities.tank.Tank):
            return self.shouldIgnoreTank(entity)
        elif entity == self.source:
            return True
        elif self.playerFiringAtBase(entity):
            return True
        
        return False

    def playerFiringAtBase(self, entity):
        return self.source.isPlayerControlled() and isinstance(entity, entities.base.Base)

    def shouldIgnoreTank(self, tank):
        return self.source.playerControlled == tank.playerControlled

    def hitByProjectile(self, projectile, time):
        self.markDisposable()

    def render(self, screen, offset, time):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))

    def getBreaksConcrete(self):
        return self.breaksConcrete
