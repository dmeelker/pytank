import pygame

import images
import utilities
from utilities import Vector

import playfield
import levels
import entities
import entities.manager
import entities.tank
import entities.base
import tankcontroller
import input

# Pygame objects
screen = None
clock = pygame.time.Clock()

running = True
lastUpdateTime = 0

playerTank = None
playerTankController = None

def start():
    initialize()

    while running:
        update()
        render()
        clock.tick(60)

def initialize():
    global screen,clock,playerTank
    pygame.init()
    pygame.display.set_caption("Pytank")
    screen = pygame.display.set_mode((320, 240)) #, pygame.FULLSCREEN)
    pygame.key.set_repeat(50, 50)

    loadImages()

    playfield.initialize(40, 30)
    loadLevel(levels.level1)

    playerTank = entities.tank.Tank(Vector(100, 100))
    playerTankController = tankcontroller.PlayerTankController(playerTank)
    playerTank.controller = playerTankController
    entities.manager.add(playerTank)
    input.tankController = playerTankController

    computerTank = entities.tank.Tank(Vector(100, 50))
    computerTank.controller = tankcontroller.AiTankController(computerTank)
    entities.manager.add(computerTank)

def loadImages():
    images.load('projectile.png', 'projectile')
    
    images.load('brick.png', 'brick')
    images.load('concrete.png', 'concrete')
    images.load('tree.png', 'tree')
    images.load('water.png', 'water')
    images.load('base.png', 'base')

    images.generateRotatedImages('tank.png', 'tank')

def loadLevel(levelString):
    lines = levelString.split('\n')

    for y in range(len(lines)):
        for x in range(playfield.width):
            character = lines[y][x]

            if character == 'B':
                playfield.setTile(x, y, playfield.Tile(images.get('brick'), blocksMovement=True, blocksProjectiles=True, destroyable=True))
            elif character == 'C':
                playfield.setTile(x, y, playfield.Tile(images.get('concrete'), blocksMovement=True, blocksProjectiles=True, destroyable=True, hitpoints=5))
            elif character == '~':
                playfield.setTile(x, y, playfield.Tile(images.get('water'), blocksMovement=True, destroyable=False))
            elif character == '^':
                playfield.setTile(x, y, playfield.Tile(images.get('tree'), blocksMovement=False, destroyable=False, layer=1))
            elif character == 'X':
                entities.manager.add(entities.base.Base(Vector(x * playfield.blockSize, y * playfield.blockSize)))

def update():
    global lastUpdateTime
    handleEvents()

    time = pygame.time.get_ticks()
    timePassed = time - lastUpdateTime
    lastUpdateTime = time

    entities.manager.update(time, timePassed)
    

def handleEvents():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            input.handleEvent(event)

def render():
    screen.fill((0, 0, 0))

    playfield.render(screen, (0, 0), layer=0)
    entities.manager.render(screen, (0, 0))
    playfield.render(screen, (0, 0), layer=1)

    pygame.display.flip()

start()

