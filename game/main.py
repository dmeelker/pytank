import os
import sys
import math
import pygame
import pygame.joystick
import pygame.freetype

import images
import fonts
import utilities
from utilities import Vector

import scenes
import scenes.gameplayscene

import input

import pathfinding.pathfindingbackgroundworker as PathfinderWorker

screen = None
screenSize = (640, 480)
bufferSize = (320, 240)
buffer = None
clock = pygame.time.Clock()
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
    initializePygame(fullscreen)
    initializeFont()
    loadImages()
    input.initialize()

    PathfinderWorker.start()

    scenes.setScene(scenes.gameplayscene.GameplayScene())

def initializePygame(fullscreen):
    pygame.init()
    pygame.key.set_repeat(50, 50)
    pygame.joystick.init()
    pygame.display.set_caption("Pytank")

    intializeDisplay(fullscreen)
    
def intializeDisplay(fullscreen):
    global screenSize, screen, buffer
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
    pygame.freetype.init()
    fonts.defaultFont = pygame.freetype.Font(os.path.join('fonts', 'DTM-Sans.otf'), size=13)
    fonts.defaultFont.antialiased = False

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

    scenes.getActiveScene().update(time, timePassed)

def handleEvents():
    global running, screenSize
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        else:
            input.handleEvent(event)

def render():
    scenes.getActiveScene().render(buffer)
    renderBufferToScreen()
    pygame.display.flip()

def renderBufferToScreen():
    pygame.transform.scale(buffer, screenSize, screen)

def frameCompleted():
    global fpsCounter, fps, lastFpsTime
    fpsCounter+=1
    if pygame.time.get_ticks() - lastFpsTime > 1000:
        lastFpsTime = pygame.time.get_ticks()
        fps = fpsCounter
        fpsCounter = 0

if __name__ == '__main__':
    start()