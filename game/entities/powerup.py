import enum
import pygame

import entities
import images
import gamecontroller

from utilities import Vector

class Powerup(entities.Entity):
    def __init__(self, image):
        super().__init__()
        self.setImage(image)
        self.creationTime = pygame.time.get_ticks()

    def update(self, time, timePassed):
        import gamecontroller

        if self.timeExpired(time):
            self.markDisposable()

        if self.boundingRectangle.colliderect(gamecontroller.getPlayerTank().boundingRectangle):
            self.apply(gamecontroller.getPlayerTank())
            self.markDisposable()

    def render(self, screen, offset, time):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))

    def apply(self, tank):
        pass

    def timeExpired(self, time):
        return time - self.creationTime > 10000

    def setImage(self, image):
        self.image = image
        self.setSize(Vector(self.image.get_width(), self.image.get_height()))

class PowerBoostPowerup(Powerup):
    def __init__(self):
        super().__init__(images.get('powerup_weapon'))

    def apply(self, tank):
        tank.getWeapon().improve()
        gamecontroller.showOverlay('Extra weapon power!')

class RepairTankPowerup(Powerup):
    def __init__(self):
        super().__init__(images.get('powerup_repairself'))

    def apply(self, tank):
        tank.repair()
        gamecontroller.showOverlay('Tank repaired!')

class RepairBasePowerup(Powerup):
    def __init__(self):
        super().__init__(images.get('powerup_repairself'))

    def apply(self, tank):
        gamecontroller.getBase().repair()
        gamecontroller.showOverlay('Base repaired!')

class DestroyAllTanksPowerup(Powerup):
    def __init__(self):
        super().__init__(images.get('powerup_destroyall'))

    def apply(self, tank):
        gamecontroller.destroyAllEnemyTanks()
        gamecontroller.showOverlay('BOOM!')

class ShieldPowerup(Powerup):
    def __init__(self):
        super().__init__(images.get('powerup_weapon'))

    def apply(self, tank):
        tank.enableShield(10000)
        gamecontroller.showOverlay('Shield!')