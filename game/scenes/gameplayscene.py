import pygame

import images
import fonts

import scenes
import gamecontroller
import playfield
import entities

from utilities import Vector

class GameplayScene(scenes.Scene):
    def __init__(self):
        gamecontroller.startNewGame()

    def activate(self):
        pass

    def deactivate(self):
        pass

    def update(self, time, timePassed):
        gamecontroller.update(time, timePassed)

    def render(self, surface):
        surface.fill((86, 79, 68))
        self.renderPlayField(surface)
        self.renderStatBar(surface)
        self.renderOverlayText(surface)

    def renderPlayField(self, targetSurface):
        playfield.renderLayer(0, targetSurface, (8, 0))
        entities.manager.render(targetSurface, (8, 0), pygame.time.get_ticks())
        playfield.renderLayer(1, targetSurface, (8, 0))

    def renderStatBar(self, targetSurface):
        targetSurface.fill((0, 0, 0), rect=pygame.Rect(0, 240 - 16, 320, 16))
        self.renderScore(targetSurface)
        self.renderLives(targetSurface)
        self.renderWeaponPower(targetSurface)
        self.renderPlayerHitpoints(targetSurface)
        self.renderBaseHitpoints(targetSurface)

    def renderScore(self, targetSurface):
        scoreSurface = fonts.defaultFont.render(f'SCORE: {gamecontroller.getScore()}', pygame.color.Color(255, 255, 255, 255))
        targetSurface.blit(scoreSurface[0], (85, 240 - 12))

    def renderLives(self, targetSurface):
        startLocation = Vector(0, 240 - 12)
        tankImage = images.get('tank1')

        for _ in range(gamecontroller.getLives()):
            targetSurface.blit(tankImage, startLocation.toIntTuple())    
            startLocation = startLocation.add(Vector(16, 0))

    def renderWeaponPower(self, targetSurface):
        image = images.get('ui_weaponpower')
        startLocation = Vector(175, 240 - 11)

        for _ in range(gamecontroller.getPlayerTank().getWeapon().getLevel()):
            targetSurface.blit(image, startLocation.toIntTuple())
            startLocation = startLocation.add(Vector(7, 0))

    def renderPlayerHitpoints(self, targetSurface):
        image = images.get('ui_heart')
        startLocation = Vector(220, 240 - 11)

        for _ in range(gamecontroller.getPlayerTank().getHitpoints()):
            targetSurface.blit(image, startLocation.toIntTuple())
            startLocation = startLocation.add(Vector(8, 0))

    def renderBaseHitpoints(self, targetSurface):
        image = images.get('ui_basehealth')
        startLocation = Vector(270, 240 - 15)
        x = startLocation.x
        y = startLocation.y

        for i in range(gamecontroller.getBase().getHitpoints()):
            targetSurface.blit(image, (x, y))

            x += 10
            if i == 4:
                x = startLocation.x
                y += 7

    def renderOverlayText(self, targetSurface):
        if gamecontroller.overlayText != None:
            age = gamecontroller.overlayHideTime - pygame.time.get_ticks()

            if int(age / 500) % 2 == 1:
                overlay = fonts.defaultFont.render(gamecontroller.overlayText, pygame.color.Color(255,255,0))
                overlaySize = overlay[1]
                location = ((targetSurface.get_width() / 2) - (overlaySize.width / 2), (targetSurface.get_height() / 2) - (overlaySize.height / 2))
                targetSurface.blit(overlay[0], location)