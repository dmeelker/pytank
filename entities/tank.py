import math
import pygame

import entities
import entities.projectile
from entities.movement import MovementHandler
import playfield

import images
from utilities import Vector
from utilities import Timer

class Tank(entities.Entity, entities.ProjectileCollider, entities.Blocking):
    heading = Vector(0, -1)
    moving = False
    hitpoints = 10
    movementSpeed = 1
    movementHandler = None
    
    imageNorth = None
    imageEast = None
    imageSouth = None
    imageWest = None

    controllerTimer = Timer(50)
    controller = None

    fireTimer = Timer(500)

    def __init__(self, location, heading = Vector(1, 0)):
        self.imageNorth = images.get('tank_north')
        self.imageEast = images.get('tank_east')
        self.imageSouth = images.get('tank_south')
        self.imageWest = images.get('tank_west')

        tileBlockedFunction = lambda tile: not tile is None and tile.blocksMovement
        self.movementHandler = MovementHandler(self, tileBlockedFunction)
        self.setLocation(location)
        self.setHeading(heading)

    def update(self, time, timePassed):
        if self.controller != None and self.controllerTimer.update(time):
            self.controller.update(time, timePassed)

        if self.moving:
            movementVector = self.heading.multiplyScalar(self.movementSpeed * timePassed * 0.05)
            self.movementHandler.moveEntity(movementVector)

        self.moving = False
        pass

    def render(self, screen, offset):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))

    def moveInDirection(self, direction):
        self.setHeading(direction)
        self.moving = True

    def canMoveInDirection(self, direction):
        return self.movementHandler.canMove(direction)

    def fire(self, time):
        if self.fireTimer.update(time):
            projectile = entities.projectile.Projectile(self.location.add(self.heading.toUnit().multiplyScalar(8)), self.heading.toUnit(), self)
            entities.manager.add(projectile)

    def hitByProjectile(self, projectile):
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