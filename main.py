import pygame

import images
import vector
import playfield
import levels
import entities
import entities.manager
import entities.tank
import entities.base

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
    loadLevel(levels.level1)

    tank = entities.tank.Tank(vector.Vector(100, 100))
    entities.manager.add(tank)

    entities.manager.add(entities.tank.Tank(vector.Vector(100, 50)))

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
                entities.manager.add(entities.base.Base(vector.Vector(x * playfield.blockSize, y * playfield.blockSize)))

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
            if event.key == pygame.K_LEFT:
                tank.moveInDirection(vector.left)
            if event.key == pygame.K_RIGHT:
                tank.moveInDirection(vector.right)
            if event.key == pygame.K_UP:
                tank.moveInDirection(vector.up)
            if event.key == pygame.K_DOWN:
                tank.moveInDirection(vector.down)
            if event.key == pygame.K_SPACE:
                tank.fire()

def render():
    screen.fill((0, 0, 0))

    playfield.render(screen, (0, 0), layer=0)
    entities.manager.render(screen, (0, 0))
    playfield.render(screen, (0, 0), layer=1)

    pygame.display.flip()

start()