import pygame
import pygame.joystick

import images
import utilities
from utilities import Vector

import playfield
import gamecontroller
import entities
import entities.manager
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
    global screen,clock
    pygame.init()
    pygame.joystick.init()
    pygame.display.set_caption("Pytank")
    screen = pygame.display.set_mode((320, 240)) #, pygame.FULLSCREEN)
    pygame.key.set_repeat(50, 50)

    input.initialize()
    gamecontroller.initialize()

    loadImages()

    gamecontroller.startNewGame()

def loadImages():
    images.load('projectile.png', 'projectile')
    
    images.load('brick.png', 'brick')
    images.load('concrete.png', 'concrete')
    images.load('tree.png', 'tree')
    images.load('water.png', 'water')
    images.load('base.png', 'base')

    images.generateRotatedImages('tank1.png', 'tank1')
    images.generateRotatedImages('tank1.png', 'tank2')
    images.generateRotatedImages('tank1.png', 'tank3')
    
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
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            input.handleEvent(event)

def render():
    screen.fill((0, 0, 0))

    playfield.renderLayer(0, screen, (0, 0))
    entities.manager.render(screen, (0, 0), pygame.time.get_ticks())
    playfield.renderLayer(1, screen, (0, 0))

    pygame.display.flip()

start()