import os
import sys
import math
import pygame
import pygame.joystick
import pygame.freetype

import images
import utilities
from utilities import Vector

import playfield
import gamecontroller
import entities
import entities.manager
import input

import pathfinding.pathfindingbackgroundworker as PathfinderWorker


# Pygame objects
screen = None
screenSize = (640, 480)
bufferSize = (320, 240)
buffer = None
clock = pygame.time.Clock()
font = None
running = True
lastUpdateTime = 0
fpsCounter = 0
lastFpsTime = 0
fps = 0

def start():
    fullscreen = True
    if len(sys.argv) > 1:
        fullscreen = sys.argv[1] == '1'

    initialize(fullscreen)

    while running:
        update()
        render()
        frameCompleted()

        clock.tick(30)

def initialize(fullscreen):
    global buffer
    pygame.init()
    pygame.key.set_repeat(50, 50)
    pygame.joystick.init()
    pygame.display.set_caption("Pytank")

    intializeDisplay(fullscreen)

    input.initialize()
    gamecontroller.initialize()

    initializeFont()
    loadImages()
    PathfinderWorker.start()

    gamecontroller.startNewGame()

def intializeDisplay(fullscreen):
    global screenSize,screen, buffer
    flags = 0

    if fullscreen:
        flags = pygame.FULLSCREEN
        screenSize = getFittingDisplaySize((320, 240), pygame.display.list_modes())
        print(f'Using resolution {screenSize}')

    screen = pygame.display.set_mode(screenSize, flags=flags)
    buffer = pygame.Surface(bufferSize)

    if fullscreen:
        pygame.mouse.set_visible(False)

def getFittingDisplaySize(baseResolution, availableSizes):
    availableSizes.reverse()
    
    for mode in availableSizes:
        if isMultipleOfBaseResolution(baseResolution, mode):
            return mode
    else:
        return getLargestFittingResolution(baseResolution, availableSizes[0])

def isMultipleOfBaseResolution(baseResolution, otherResolution):
    return otherResolution[0] % baseResolution[0] == 0 and \
        otherResolution[1] % baseResolution[1] == 0

def getLargestFittingResolution(baseResolution, screenResolution):
    horizontalFactor = int(screenResolution[0] / baseResolution[0])
    verticalFactor = int(screenResolution[1] / baseResolution[1])
    factor = min(horizontalFactor, verticalFactor)
    return (baseResolution[0] * factor, baseResolution[1] * factor)

def initializeFont():
    global font
    pygame.freetype.init()
    font = pygame.freetype.Font(os.path.join('fonts', 'DTM-Sans.otf'), size=13)
    font.antialiased = False

def loadImages():
    images.load('projectile.png')
    
    images.load('brick.png')
    images.load('concrete.png')
    images.load('tree.png')
    images.load('water.png')
    images.load('base.png')
    images.load('tank1.png')

    images.load('ui_weaponpower.png')
    images.load('ui_heart.png')
    images.load('ui_basehealth.png')

    images.load('powerup_weapon.png')
    images.load('powerup_destroyall.png')
    images.load('powerup_repairself.png')
    images.load('powerup_repairbase.png')

    images.generateRotatedImages('tank1_base.png')
    images.generateRotatedImages('tank1_turret.png')

    images.generateRotatedImages('tank2_base.png')
    images.generateRotatedImages('tank2_turret.png')

    images.generateRotatedImages('tank3_base.png')
    images.generateRotatedImages('tank3_turret.png')

    images.generateRotatedImages('tank4_base.png')
    images.generateRotatedImages('tank4_turret.png')

    images.generateRotatedImages('projectile.png')

    images.generateRotatedImages('tank1.png')
    
def update():
    global lastUpdateTime
    handleEvents()
    input.update()

    time = pygame.time.get_ticks()
    timePassed = time - lastUpdateTime
    lastUpdateTime = time

    gamecontroller.update(time, timePassed)

def handleEvents():
    global running, screenSize
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        else:
            input.handleEvent(event)

def render():
    renderToSurface(buffer)
    pygame.transform.scale(buffer, screenSize, screen)

    pygame.display.flip()

def renderToSurface(targetSurface):
    targetSurface.fill((86, 79, 68))
    renderPlayField(targetSurface)
    renderStatBar(targetSurface)
    renderOverlayText(targetSurface)

def renderPlayField(targetSurface):
    playfield.renderLayer(0, targetSurface, (8, 0))
    entities.manager.render(targetSurface, (8, 0), pygame.time.get_ticks())
    playfield.renderLayer(1, targetSurface, (8, 0))

def renderStatBar(targetSurface):
    targetSurface.fill((0, 0, 0), rect=pygame.Rect(0, 240 - 16, 320, 16))
    renderScore(targetSurface)
    renderLives(targetSurface)
    renderWeaponPower(targetSurface)
    renderPlayerHitpoints(targetSurface)
    renderBaseHitpoints(targetSurface)

def renderScore(targetSurface):
    scoreSurface = font.render(f'SCORE: {gamecontroller.getScore()}', pygame.color.Color(255, 255, 255, 255))
    targetSurface.blit(scoreSurface[0], (85, 240 - 12))

def renderLives(targetSurface):
    startLocation = Vector(0, 240 - 12)
    tankImage = images.get('tank1')

    for _ in range(gamecontroller.getLives()):
        targetSurface.blit(tankImage, startLocation.toIntTuple())    
        startLocation = startLocation.add(Vector(16, 0))

def renderWeaponPower(targetSurface):
    image = images.get('ui_weaponpower')
    startLocation = Vector(175, 240 - 11)

    for _ in range(gamecontroller.getPlayerTank().getWeapon().getLevel()):
        targetSurface.blit(image, startLocation.toIntTuple())
        startLocation = startLocation.add(Vector(7, 0))

def renderPlayerHitpoints(targetSurface):
    image = images.get('ui_heart')
    startLocation = Vector(220, 240 - 11)

    for _ in range(gamecontroller.getPlayerTank().getHitpoints()):
        targetSurface.blit(image, startLocation.toIntTuple())
        startLocation = startLocation.add(Vector(8, 0))

def renderBaseHitpoints(targetSurface):
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

def renderOverlayText(targetSurface):
    if gamecontroller.overlayText != None:
        age = gamecontroller.overlayHideTime - pygame.time.get_ticks()

        if int(age / 500) % 2 == 1:
            overlay = font.render(gamecontroller.overlayText, pygame.color.Color(255,255,0))
            overlaySize = overlay[1]
            location = ((bufferSize[0] / 2) - (overlaySize.width / 2), (bufferSize[1] / 2) - (overlaySize.height / 2))
            targetSurface.blit(overlay[0], location)

def frameCompleted():
    global fpsCounter, fps, lastFpsTime
    fpsCounter+=1
    if pygame.time.get_ticks() - lastFpsTime > 1000:
        lastFpsTime = pygame.time.get_ticks()
        fps = fpsCounter
        fpsCounter = 0

if __name__ == '__main__':
    start()