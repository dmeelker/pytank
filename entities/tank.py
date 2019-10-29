import math
import pygame

import entities
import entities.projectile
from entities.movement import MovementHandler
import playfield

import images
from vector import Vector

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

    def __init__(self, location, heading = Vector(1, 0)):
        self.imageNorth = images.get('tank_north')
        self.imageEast = images.get('tank_east')
        self.imageSouth = images.get('tank_south')
        self.imageWest = images.get('tank_west')

        self.movementHandler = MovementHandler(self)
        self.setLocation(location)
        self.setHeading(heading)

    def update(self, time, timePassed):
        if self.moving:
            movementVector = self.heading.multiplyScalar(self.movementSpeed * timePassed * 0.2)
            self.movementHandler.moveEntity(movementVector)

        self.moving = False
        pass

    def render(self, screen, offset):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))

    def moveLeft(self):
        self.moveToVector(Vector(-1, 0))

    def moveRight(self):
        self.moveToVector(Vector(1, 0))

    def moveUp(self):
        self.moveToVector(Vector(0, -1))

    def moveDown(self):
        self.moveToVector(Vector(0, 1))

    def moveToVector(self, vector):
        self.setHeading(vector)
        self.moving = True

    def fire(self):
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