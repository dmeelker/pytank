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
    def __init__(self, location, heading = Vector(1, 0)):
        super().__init__()
        self.imageNorth = images.get('tank_north')
        self.imageEast = images.get('tank_east')
        self.imageSouth = images.get('tank_south')
        self.imageWest = images.get('tank_west')

        self.heading = Vector(0, -1)
        self.moving = False
        self.hitpoints = 10

        self.controller = None
        self.controllerTimer = Timer(50)
        self.fireTimer = Timer(500)

        tileBlockedFunction = lambda tile: not tile is None and tile.blocksMovement
        self.movementHandler = MovementHandler(self, tileBlockedFunction)
        self.movementSpeed = 1
        self.setLocation(location)
        self.setHeading(heading)
        self.lastHitTime = None
        self.lastHitVector = Vector(0, 0)

    def setController(self, controller):
        self.controller = controller
        self.playerControlled = isinstance(controller, tankcontroller.PlayerTankController)

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
        if self.fireTimer.update(time):
            projectile = entities.projectile.Projectile(Vector(0, 0), self.heading.toUnit(), self)

            centerLocation = self.getCenterLocation()
            location = centerLocation.subtract(projectile.size.multiplyScalar(0.5)).add(self.heading.toUnit().multiplyScalar(6))
            projectile.setLocation(location)

            entities.manager.add(projectile)

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

    def destroy(self):
        self.markDisposable()