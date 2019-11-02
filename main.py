import pygame
import pygame.joystick

import images
import utilities
from utilities import Vector

import playfield
import levelcontroller
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

    levelcontroller.loadLevel(levels.level1)

def loadImages():
    images.load('projectile.png', 'projectile')
    
    images.load('brick.png', 'brick')
    images.load('concrete.png', 'concrete')
    images.load('tree.png', 'tree')
    images.load('water.png', 'water')
    images.load('base.png', 'base')

    images.generateRotatedImages('tank.png', 'tank')
    
def update():
    global lastUpdateTime
    handleEvents()
    input.update()

    time = pygame.time.get_ticks()
    timePassed = time - lastUpdateTime
    lastUpdateTime = time

    entities.manager.update(time, timePassed)
    levelcontroller.update(time, timePassed)

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
    entities.manager.render(screen, (0, 0), pygame.time.get_ticks())
    playfield.render(screen, (0, 0), layer=1)

    pygame.display.flip()

start()

