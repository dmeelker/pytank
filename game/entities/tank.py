import enum
import math
import pygame

import entities
from entities import Direction
import entities.projectile
from entities.movement import MovementHandler
import playfield
import tankcontroller

import images
from utilities import Vector
from utilities import Timer

class Tank(entities.Entity, entities.ProjectileCollider, entities.Blocking):
    def __init__(self, location, graphics, heading = Vector(1, 0)):
        super().__init__()
        self.graphics = graphics

        self.heading = Vector(0, -1)
        self.direction = Direction.NORTH
        self.moving = False
        self.type = type

        self.maxHitPoints = 10
        self.hitpoints = self.maxHitPoints
        self.movementSpeed = 1
        self.scorePoints = 0

        self.shielded = False
        self.shieldEndTime = 0

        self.weapon = Weapon(self, level=1)

        self.controller = None
        self.controllerTimer = Timer(50)

        tileBlockedFunction = lambda tile: not tile is None and tile.blocksMovement
        self.movementHandler = MovementHandler(self, tileBlockedFunction)
        
        self.setLocation(location)
        self.setHeading(heading)
        self.lastHitTime = None
        self.lastHitVector = Vector(0, 0)
        self.destroyCallback = None
        self.destroyed = False

    def setScorePoints(self, points):
        self.scorePoints = points

    def getScorePoints(self):
        return self.scorePoints

    def setMaxHitpoints(self, hitpoints):
        self.maxHitPoints = hitpoints
        self.repair()

    def repair(self):
        self.hitpoints = self.maxHitPoints

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
            movementVector = self.heading.multiplyScalar(self.movementSpeed * timePassed * 0.05).round()
            self.movementHandler.moveEntity(movementVector)

        self.checkIfShieldIsDone(time)

        self.moving = False
        pass

    def render(self, screen, offset, time):
        extraOffset = Vector(0, 0) 
        
        if not self.lastHitTime == None and time - self.lastHitTime > 50:
            extraOffset = self.lastHitVector.multiplyScalar(-1).toUnit()
        
        drawOffset = Vector(offset[0], offset[1])
        self.graphics.render(screen, drawOffset.add(self.location).add(extraOffset), self.direction)
        self.controller.render(screen)

    def moveSingleStep(self, direction):
        self.setHeading(direction)
        self.movementHandler.moveEntity(direction.toUnit())

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
        halfProjectileSize = Vector(2, 2)
        location = self.getCenterLocation()

        return location.subtract(halfProjectileSize)
        # halfProjectileSize = Vector(2, 2)
        # location = self.getCenterLocation()
        # location = location.subtract(halfProjectileSize)
        # location = location.add(self.heading.toUnit().multiplyScalar(self.size.y / 2))
        # return location

    def hitByProjectile(self, projectile, time):
        if self.shielded:
            return
        
        self.lastHitTime = time
        self.lastHitVector = projectile.directionVector

        self.hitpoints -= projectile.power
        if self.hitpoints <= 0:
            self.destroy()

    def setImage(self, image):
        self.image = image
        self.setSize(Vector(self.image.get_width(), self.image.get_height()))

    def getHeading(self):
        return self.heading

    def setHeading(self, newHeading):
        self.heading = newHeading
        self.direction = self.getDirectionFromVector(self.heading)
        self.setGraphics(self.direction)

    def setGraphics(self, direction):
        self.setImage(self.graphics.baseImages[direction])
        self.turretImage = self.graphics.turretImages[direction]
        self.turretOffset = self.graphics.turretOffsets[direction]


    def getWeapon(self):
        return self.weapon

    def setWeapon(self, newWeapon):
        self.weapon = newWeapon

    def enableShield(self, duration):
        self.shielded = True
        self.shieldEndTime = pygame.time.get_ticks() + duration
        print(f'Shield enabled for {duration} seconds')

    def checkIfShieldIsDone(self, time):
        if self.shielded and time >= self.shieldEndTime:
            self.shielded = False
            print('Shield has ran out')

    def setDestroyCallback(self, callback):
        self.destroyCallback = callback

    def fireDestroyCallback(self):
        if self.destroyCallback != None:
            self.destroyCallback(self)

    def getHitpoints(self):
        return self.hitpoints

    def destroy(self):
        self.destroyed = True
        self.fireDestroyCallback()
        self.markDisposable()

    def isDestroyed(self):
        return self.destroyed

class Weapon:
    def __init__(self, entity, level):
        self.entity = entity
        self.lastFireTime = 0
        self.fireRateModifier = 1
        self.setLevel(level)

    def getLevel(self):
        return self.level

    def setLevel(self, level):
        self.level = level
        self.fireDelay = 1000 * self.fireRateModifier
        self.power = 1
        self.breaksConcrete = False

        if level >= 2:
            self.fireDelay = 500 * self.fireRateModifier
        if level >= 3:
            self.power = 2
        if level >= 4:
            self.breaksConcrete = True

    def improve(self):
        if self.level < 4:
            self.setLevel(self.level + 1)

    def canFire(self, time):
        return time - self.lastFireTime > self.fireDelay

    def fire(self, location, vector, time):
        if not self.canFire(time):
            return

        self.lastFireTime = time
        projectile = entities.projectile.Projectile(Vector(0, 0), vector.toUnit(), source=self.entity, power=self.power, breaksConcrete=self.breaksConcrete)
        projectile.setLocation(location)
        entities.manager.add(projectile)

    def setFireRateModifier(self, rate):
        self.fireRateModifier = rate
        self.setLevel(self.level)

class TankGraphics:
    def __init__(self, type, turretOffsets):
        self.baseImages = { \
            Direction.NORTH: images.get(f'tank{type}_base_north'), \
            Direction.EAST: images.get(f'tank{type}_base_east'), \
            Direction.SOUTH: images.get(f'tank{type}_base_south'), \
            Direction.WEST: images.get(f'tank{type}_base_west')}

        self.turretImages = { \
            Direction.NORTH: images.get(f'tank{type}_turret_north'), \
            Direction.EAST: images.get(f'tank{type}_turret_east'), \
            Direction.SOUTH: images.get(f'tank{type}_turret_south'), \
            Direction.WEST: images.get(f'tank{type}_turret_west')}

        self.turretOffsets = turretOffsets

    def render(self, surface, location, direction):
        baseImage = self.baseImages[direction]
        turretImage = self.turretImages[direction]
        turretOffset = self.turretOffsets[direction]

        surface.blit(baseImage, (location.x, location.y))
        surface.blit(turretImage, (location.x + turretOffset.x, location.y + turretOffset.y))

    @staticmethod
    def createPlayerTank():
        turretOffsets = { \
            Direction.NORTH: Vector(3, -3), \
            Direction.EAST: Vector(4, 3), \
            Direction.SOUTH: Vector(3, 4), \
            Direction.WEST: Vector(-3, 3)}

        return TankGraphics(1, turretOffsets)

    @staticmethod
    def createEnemyTank1():
        turretOffsets = { \
            Direction.NORTH: Vector(3, -1), \
            Direction.EAST: Vector(2, 3), \
            Direction.SOUTH: Vector(3, 1), \
            Direction.WEST: Vector(-1, 3)}

        return TankGraphics(2, turretOffsets)

    @staticmethod
    def createEnemyTank2():
        turretOffsets = { \
            Direction.NORTH: Vector(3, -2), \
            Direction.EAST: Vector(4, 3), \
            Direction.SOUTH: Vector(3, 4), \
            Direction.WEST: Vector(-2, 3)}

        return TankGraphics(3, turretOffsets)

    @staticmethod
    def createEnemyTank3():
        turretOffsets = { \
            Direction.NORTH: Vector(3, -3), \
            Direction.EAST: Vector(2, 3), \
            Direction.SOUTH: Vector(3, 2), \
            Direction.WEST: Vector(-3, 3)}

        return TankGraphics(4, turretOffsets)