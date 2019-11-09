import enum

import entities
import images
import gamecontroller

from utilities import Vector

class Powerup(entities.Entity):
    def __init__(self, location):
        super().__init__()
        self.setLocation(location)

    def update(self, time, timePassed):
        if self.boundingRectangle.colliderect(gamecontroller.getPlayerTank().boundingRectangle):
            self.apply(gamecontroller.getPlayerTank())
            self.markDisposable()

    def render(self, screen, offset, time):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))

    def apply(self, tank):
        pass

    def setImage(self, image):
        self.image = image
        self.setSize(Vector(self.image.get_width(), self.image.get_height()))

class PowerBoostPowerup(Powerup):
    def __init__(self, location):
        super().__init__(location)
        self.setImage(images.get('powerup'))

    def apply(self, tank):
        tank.getWeapon().improve()