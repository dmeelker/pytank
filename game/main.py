import os

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
    initialize()

    while running:
        update()
        render()
        frameCompleted()

        clock.tick(30)

def initialize():
    global screen,clock, buffer
    pygame.init()
    pygame.joystick.init()
    pygame.display.set_caption("Pytank")
    screen = pygame.display.set_mode((640, 480)) # , pygame.FULLSCREEN)
    pygame.key.set_repeat(50, 50)

    buffer = pygame.Surface(bufferSize)

    input.initialize()
    gamecontroller.initialize()

    initializeFont()
    loadImages()
    
    PathfinderWorker.start()

    gamecontroller.startNewGame()

def initializeFont():
    global font
    pygame.freetype.init()
    font = pygame.freetype.Font(os.path.join('fonts', 'DTM-Sans.otf'), size=13)
    font.antialiased = False

def loadImages():
    images.load('projectile.png', 'projectile')
    
    images.load('brick.png', 'brick')
    images.load('concrete.png', 'concrete')
    images.load('tree.png', 'tree')
    images.load('water.png', 'water')
    images.load('base.png', 'base')
    images.load('tank1.png', 'tank1')

    images.load('powerup_weapon.png', 'powerup_weapon')
    images.load('powerup_destroyall.png', 'powerup_destroyall')
    images.load('powerup_repairself.png', 'powerup_repairself')

    images.generateRotatedImages('tank1.png', 'tank1')
    images.generateRotatedImages('tank1.png', 'tank2')
    images.generateRotatedImages('tank1.png', 'tank3')
    images.generateRotatedImages('tank1.png', 'tank4')
    
def update():
    global lastUpdateTime
    handleEvents()
    input.update()

    time = pygame.time.get_ticks()
    timePassed = time - lastUpdateTime
    lastUpdateTime = time

    entities.manager.update(time, timePassed)
    gamecontroller.update(time, timePassed)

def handleEvents():
    global running, screenSize
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screenSize = event.size
            print(f'New screen size: {screenSize}')
        else:
            input.handleEvent(event)



def render():
    renderToSurface(buffer)
    pygame.transform.scale(buffer, screenSize, screen)

    pygame.display.flip()

def renderToSurface(targetSurface):
    targetSurface.fill((0, 0, 0))

    playfield.renderLayer(0, targetSurface, (0, 0))
    entities.manager.render(targetSurface, (0, 0), pygame.time.get_ticks())
    playfield.renderLayer(1, targetSurface, (0, 0))

    scoreSurface = font.render(f'SCORE: {gamecontroller.getScore()}', pygame.color.Color(255, 255, 255, 255))
    targetSurface.blit(scoreSurface[0], (75, 240 - 12))

    renderLives(targetSurface)
    renderWeaponPower(targetSurface)
    renderPlayerHitpoints(targetSurface)
    renderBaseHitpoints(targetSurface)
    renderOverlayText(targetSurface)

def renderLives(targetSurface):
    startLocation = Vector(0, 240 - 12)
    tankImage = images.get('tank1')

    for _ in range(gamecontroller.getLives()):
        targetSurface.blit(tankImage, startLocation.toIntTuple())    
        startLocation = startLocation.add(Vector(16, 0))

def renderWeaponPower(targetSurface):
    image = images.get('projectile')
    startLocation = Vector(160, 240 - 12)

    for _ in range(gamecontroller.getPlayerTank().getWeapon().getLevel()):
        targetSurface.blit(image, startLocation.toIntTuple())
        startLocation = startLocation.add(Vector(4, 0))

def renderPlayerHitpoints(targetSurface):
    image = images.get('projectile')
    startLocation = Vector(210, 240 - 12)

    for _ in range(gamecontroller.getPlayerTank().getHitpoints()):
        targetSurface.blit(image, startLocation.toIntTuple())
        startLocation = startLocation.add(Vector(4, 0))

def renderBaseHitpoints(targetSurface):
    image = images.get('projectile')
    startLocation = Vector(260, 240 - 12)

    for _ in range(gamecontroller.getBase().getHitpoints()):
        targetSurface.blit(image, startLocation.toIntTuple())
        startLocation = startLocation.add(Vector(4, 0))

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

start()