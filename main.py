import pygame
import pygame.joystick

import images
import utilities
from utilities import Vector

import playfield
import levels
import entities
import entities.manager
import entities.tank
import entities.base
from tankspawner import TankSpawner
import tankcontroller
import input

# Pygame objects
screen = None
clock = pygame.time.Clock()

running = True
lastUpdateTime = 0

playerTank = None
playerTankController = None

# Level objects
tankSpawners = []
base = None

def start():
    initialize()

    while running:
        update()
        render()
        clock.tick(60)

def initialize():
    global screen,clock,playerTank
    pygame.init()
    pygame.joystick.init()
    pygame.display.set_caption("Pytank")
    screen = pygame.display.set_mode((320, 240)) #, pygame.FULLSCREEN)
    pygame.key.set_repeat(50, 50)

    input.initialize()

    loadImages()

    playfield.initialize(40, 30)

    loadLevel(levels.level1)

def loadImages():
    images.load('projectile.png', 'projectile')
    
    images.load('brick.png', 'brick')
    images.load('concrete.png', 'concrete')
    images.load('tree.png', 'tree')
    images.load('water.png', 'water')
    images.load('base.png', 'base')

    images.generateRotatedImages('tank.png', 'tank')

def loadLevel(levelString):
    global tankSpawners, base
    entities.manager.clear()
    
    playerTank = entities.tank.Tank(Vector(100, 100))
    playerTank.fireTimer.setInterval(100)
    playerTank.movementSpeed = 3
    playerTankController = tankcontroller.PlayerTankController(playerTank)
    playerTank.setController(playerTankController)
    entities.manager.add(playerTank)
    input.tankController = playerTankController

    lines = levelString.split('\n')
    tankSpawners = []

    for y in range(len(lines)):
        for x in range(playfield.width):
            character = lines[y][x]
            pixelLocation = Vector(x * playfield.blockSize, y * playfield.blockSize)

            if character == 'B':
                playfield.setTile(x, y, playfield.Tile(images.get('brick'), blocksMovement=True, blocksProjectiles=True, destroyable=True))
            elif character == 'C':
                playfield.setTile(x, y, playfield.Tile(images.get('concrete'), blocksMovement=True, blocksProjectiles=True, destroyable=True, hitpoints=5))
            elif character == '~':
                playfield.setTile(x, y, playfield.Tile(images.get('water'), blocksMovement=True, destroyable=False))
            elif character == '^':
                playfield.setTile(x, y, playfield.Tile(images.get('tree'), blocksMovement=False, destroyable=False, layer=1))
            elif character == 'X':
                base = entities.base.Base(pixelLocation)
                entities.manager.add(base)
            elif character == 'P':
                playerTank.setLocation(pixelLocation)
                playerTank.setHeading(utilities.vectorUp)
            elif character == 'S':
                tankSpawners.append(TankSpawner(pixelLocation))

def update():
    global lastUpdateTime
    handleEvents()
    input.update()

    time = pygame.time.get_ticks()
    timePassed = time - lastUpdateTime
    lastUpdateTime = time

    entities.manager.update(time, timePassed)
    updateTankSpawners(time, timePassed)
    
    if base.disposed:
        loadLevel(levels.level1)

def handleEvents():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            input.handleEvent(event)

def updateTankSpawners(time, timePassed):
    for tankSpawner in tankSpawners:
        tankSpawner.update(time, timePassed)

def render():
    screen.fill((0, 0, 0))

    playfield.render(screen, (0, 0), layer=0)
    entities.manager.render(screen, (0, 0))
    playfield.render(screen, (0, 0), layer=1)

    pygame.display.flip()

start()

