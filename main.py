import pygame

import images
import vector
import playfield
import entities
import entities.manager
import entities.tank

# Pygame objects
screen = None
clock = pygame.time.Clock()

running = True
lastUpdateTime = 0

tank = None

def start():
    initialize()

    while running:
        update()
        render()
        clock.tick(60)

def initialize():
    global screen,clock,tank
    pygame.init()
    pygame.display.set_caption("Pytank")
    screen = pygame.display.set_mode((320, 240)) #, pygame.FULLSCREEN)
    pygame.key.set_repeat(50, 50)

    loadImages()

    playfield.initialize(40, 30)

    for x in range(4, playfield.width - 8):
        for y in range(4, 4 + 2):
            playfield.setTile(x, y, playfield.Tile(images.get('brick'), blocksMovement=True, destroyable=True))

    tank = entities.tank.Tank(vector.Vector(100, 100))
    entities.manager.add(tank)

    entities.manager.add(entities.tank.Tank(vector.Vector(100, 50)))

def loadImages():
    images.load('projectile.png', 'projectile')
    images.load('brick.png', 'brick')
    images.load('concrete.png', 'concrete')

    images.generateRotatedImages('tank.png', 'tank')

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                tank.moveLeft()
            elif event.key == pygame.K_RIGHT:
                tank.moveRight()
            elif event.key == pygame.K_UP:
                tank.moveUp()
            elif event.key == pygame.K_DOWN:
                tank.moveDown()
            elif event.key == pygame.K_SPACE:
                tank.fire()

def render():
    screen.fill((0, 0, 0))

    playfield.render(screen, (0, 0))
    entities.manager.render(screen, (0, 0))

    pygame.display.flip()

start()