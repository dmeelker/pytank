import pygame
import pygame.time

import images
import fonts
import input
import scenes
import scenes.gameplayscene

class TitleScene(scenes.Scene):
    def __init__(self):
        pass

    def activate(self):
        pass

    def deactivate(self):
        pass

    def update(self, time, timePassed):
        if input.buttonStates.fire:
            scenes.setScene(scenes.gameplayscene.GameplayScene())
            pygame.time.wait(200)

    def render(self, surface):
        surface.fill((86, 79, 68))
        self.renderHeader(surface)
        self.renderOutline(surface)
        self.renderText(surface)

    def renderHeader(self, surface):
        data = [\
            'XXX X   X XXXXX   X   X   X X  X', \
            'X X  X X    X    X X  XX  X X X ', \
            'XXX   X     X    X X  X X X XX  ', \
            'X     X     X   XXXXX X  XX X X ', \
            'X     X     X   X   X X   X X  X', \
        ]

        self.renderTileGrid(surface, data, (4, 2))

    def renderTileGrid(self, surface, dataArray, location):
        image = images.get('brick')
        width = len(dataArray[0])
        height = len(dataArray)

        for y in range(height):
            line = dataArray[y]
            for x in range(width):
                if line[x] == 'X':
                    surface.blit(image, ((x + location[0]) * 8, (y + location[1]) * 8))


    def renderOutline(self, surface):
        image = images.get('concrete')
        screenSize = (int(320 / 8), int(240 / 8))

        self.drawCenteredRectangle(surface, image, 20, 6, screenSize)

    def renderText(self, surface):
        scoreSurface = fonts.defaultFont.render(f'Hit FIRE to start!', pygame.color.Color(255, 255, 255, 255))
        location = ((320 / 2) - (scoreSurface[1].width / 2), (240 / 2) - (scoreSurface[1].height / 2))
        surface.blit(scoreSurface[0], location)
        
    def drawHorizontalLine(self, surface, image, x, y, length):
        for currentX in range(length):
            surface.blit(image, ((x + currentX) * 8, y * 8))

    def drawVerticalLine(self, surface, image, x, y, length):
        for currentY in range(length):
            surface.blit(image, (x * 8, (y + currentY) * 8))

    def drawRectangle(self, surface, image, x, y, width, height):
        self.drawHorizontalLine(surface, image, x, y, width)
        self.drawHorizontalLine(surface, image, x, y + (height - 1), width)
        self.drawVerticalLine(surface, image, x, y, height)
        self.drawVerticalLine(surface, image, x + (width - 1), y, height)

    def drawCenteredRectangle(self, surface, image, width, height, screenSize):
        self.drawRectangle(surface, image, (screenSize[0] / 2) - int(width / 2), (screenSize[1] / 2) - int(height / 2), width, height)