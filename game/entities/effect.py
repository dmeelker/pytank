import pygame.time
import entities

from utilities import Vector

class Effect(entities.Entity):
    def __init__(self, image, location, duration):
        super().__init__()
        self.image = image
        self.setSize(Vector(self.image.get_width(), self.image.get_height()))
        self.centerOn(location)
        self.creationTime = pygame.time.get_ticks()
        self.duration = duration

    def update(self, time, timePassed):
        if time - self.creationTime > self.duration:
            self.markDisposable()

    def render(self, screen, offset, time):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))