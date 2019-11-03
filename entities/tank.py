import math
import pygame

import entities
import entities.projectile
from entities.movement import MovementHandler
import playfield
import tankcontroller

import images
from utilities import Vector
from utilities import Timer

class Tank(entities.Entity, entities.ProjectileCollider, entities.Blocking):
    def __init__(self, location, type, heading = Vector(1, 0)):
        super().__init__()
        self.imageNorth = images.get(f'tank{type}_north')
        self.imageEast = images.get(f'tank{type}_east')
        self.imageSouth = images.get(f'tank{type}_south')
        self.imageWest = images.get(f'tank{type}_west')

        self.heading = Vector(0, -1)
        self.moving = False
        self.type = type

        self.hitpoints = 10
        self.movementSpeed = 1

        self.weapon = Weapon(self)

        self.controller = None
        self.controllerTimer = Timer(50)

        tileBlockedFunction = lambda tile: not tile is None and tile.blocksMovement
        self.movementHandler = MovementHandler(self, tileBlockedFunction)
        
        self.setLocation(location)
        self.setHeading(heading)
        self.lastHitTime = None
        self.lastHitVector = Vector(0, 0)
        self.destroyCallback = None

    def getScorePoints(self):
        return self.type * 100

    def setController(self, controller):
        self.controller = controller
        self.playerControlled = isinstance(controller, tankcontroller.PlayerTankController)

    def getController(self):
        return self.controller

    def isPlayerControlled(self):
        return self.playerControlled

    def update(self, time, timePassed):
        if self.controllerTimer.update(time):
            self.controller.update(time, timePassed)

        if self.moving:
            movementVector = self.heading.multiplyScalar(self.movementSpeed * timePassed * 0.05)
            self.movementHandler.moveEntity(movementVector)

        self.moving = False
        pass

    def render(self, screen, offset, time):
        extraOffset = Vector(0, 0) 
        
        if not self.lastHitTime == None and time - self.lastHitTime > 50:
            extraOffset = self.lastHitVector.multiplyScalar(-1).toUnit()
        
        screen.blit(self.image, (offset[0] + extraOffset.x + self.location.x, offset[1] + extraOffset.y + self.location.y))

    def moveInDirection(self, direction):
        self.setHeading(direction)
        self.moving = True

    def canMoveInDirection(self, direction):
        return self.movementHandler.canMove(direction)

    def fire(self, time):
        if self.weapon.canFire(time):
            location = self.getProjectileFireLocation()
            self.weapon.fire(location, self.heading, time)

    def getProjectileFireLocation(self):
        halfProjectileSize = Vector(4, 4)
        location = self.getCenterLocation()
        location = location.subtract(halfProjectileSize)
        location = location.add(self.heading.toUnit().multiplyScalar(self.size.y / 2))
        return location

    def hitByProjectile(self, projectile, time):
        self.lastHitTime = time
        self.lastHitVector = projectile.directionVector

        self.hitpoints -= projectile.power
        if self.hitpoints <= 0:
            self.destroy()

    def setImage(self, image):
        self.image = image
        self.setSize(Vector(self.image.get_width(), self.image.get_height()))

    def setHeading(self, newHeading):
        self.heading = newHeading
        self.updateImageBasedOnHeading()

    def updateImageBasedOnHeading(self):
        if self.heading.y < 0:
            self.setImage(self.imageNorth)
        elif self.heading.y > 0:
            self.setImage(self.imageSouth)
        elif self.heading.x < 0:
            self.setImage(self.imageWest)
        elif self.heading.x > 0:
            self.setImage(self.imageEast)

    def setWeapon(self, newWeapon):
        self.weapon = newWeapon

    def setDestroyCallback(self, callback):
        self.destroyCallback = callback

    def fireDestroyCallback(self):
        if self.destroyCallback != None:
            self.destroyCallback(self)

    def destroy(self):
        self.fireDestroyCallback()
        self.markDisposable()

class Weapon:
    def __init__(self, entity):
        self.entity = entity
        self.lastFireTime = 0
        self.fireDelay = 500

    def canFire(self, time):
        return time - self.lastFireTime > self.fireDelay

    def fire(self, location, vector, time):
        if not self.canFire(time):
            return

        self.lastFireTime = time
        projectile = entities.projectile.Projectile(Vector(0, 0), vector.toUnit(), source=self.entity, power=1)
        projectile.setLocation(location)
        entities.manager.add(projectile)
