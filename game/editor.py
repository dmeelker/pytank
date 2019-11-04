import sys
import os
import pygame
import images
import playfield

# Pygame objects
screen = None
clock = pygame.time.Clock()

running = True
lastUpdateTime = 0

brickTile = None
concreteTile = None
waterTile = None
treeTile = None
activeTile = None

baseLocation = (18, 28)
tankSpawners = []
playerStartLocation = (18, 25)

openFileName = None
tankSpawnOrder = '0 0 0 0 0'

def start():
    initialize()

    if len(sys.argv) > 1:
        processCommandLineArgument(sys.argv[1])

    while running:
        update()
        render()
        clock.tick(60)

def processCommandLineArgument(fileName):
    global openFileName
    openFileName = fileName

    if os.path.exists(fileName):
        loadLevelFile(fileName)

def initialize():
    global screen,clock
    pygame.init()
    pygame.display.set_caption("Pytank Editor")
    screen = pygame.display.set_mode((320, 240)) #, pygame.FULLSCREEN)
    playfield.initialize()
    loadImages()
    initializeTiles()

def initializeTiles():
    global brickTile, concreteTile, waterTile, treeTile
    brickTile = playfield.Tile(playfield.TileType.BRICK)
    concreteTile = playfield.Tile(playfield.TileType.CONCRETE)
    waterTile = playfield.Tile(playfield.TileType.WATER)
    treeTile = playfield.Tile(playfield.TileType.TREE)
    setActiveTile(treeTile)

def setActiveTile(tile):
    global activeTile
    activeTile = tile

def loadImages():
    images.load('projectile.png', 'projectile')
    
    images.load('brick.png', 'brick')
    images.load('concrete.png', 'concrete')
    images.load('tree.png', 'tree')
    images.load('water.png', 'water')
    images.load('base.png', 'base')

    images.load('tank1.png', 'tank1')
    images.load('tank3.png', 'tank3')
    
def update():
    handleEvents()

    mouseLocation = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:        
        drawTileAtPixel(mouseLocation[0], mouseLocation[1], activeTile)
    if pygame.mouse.get_pressed()[2]:        
        drawTileAtPixel(mouseLocation[0], mouseLocation[1], None)

def drawTileAtPixel(x, y, tileType):
    tileX = int(x / playfield.blockSize)
    tileY = int(y / playfield.blockSize)

    playfield.setTile(tileX, tileY, tileType)

def handleEvents():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                setActiveTile(brickTile)
            elif event.key == pygame.K_2:
                setActiveTile(concreteTile)
            elif event.key == pygame.K_3:
                setActiveTile(waterTile)
            elif event.key == pygame.K_4:
                setActiveTile(treeTile)
            elif event.key == pygame.K_s:
                toggleTanksSpawnerAtMouseLocation()
            elif event.key == pygame.K_b:
                moveBaseToMouseLocation()
            elif event.key == pygame.K_p:
                movePlayerSpawnToMouseLocation()
            elif event.key == pygame.K_F1:
                writeLevelFile(openFileName)

def toggleTanksSpawnerAtMouseLocation():
    tileLocation = getMouseTileLocation()
    tankSpawnerAtLocation = findTankSpawnerAtTile(tileLocation)

    if tankSpawnerAtLocation is None:
        tankSpawners.append(tileLocation)
    else:
        tankSpawners.remove(tankSpawnerAtLocation)

def findTankSpawnerAtTile(tileLocation):
    for tankSpawner in tankSpawners:
        if tankSpawner == tileLocation:
            return tankSpawner
    else:
        return None

def moveBaseToMouseLocation():
    global baseLocation
    baseLocation = getMouseTileLocation()

def movePlayerSpawnToMouseLocation():
    global playerStartLocation
    playerStartLocation = getMouseTileLocation()

def getMouseTileLocation():
    mouseLocation = pygame.mouse.get_pos()
    return (int(mouseLocation[0] / playfield.blockSize), int(mouseLocation[1] / playfield.blockSize))

def render():
    screen.fill((0, 0, 0))

    screen.blit(images.get('base'), (baseLocation[0] * playfield.blockSize, baseLocation[1] * playfield.blockSize))
    playfield.renderLayer(0, screen, (0, 0))
    playfield.renderLayer(1, screen, (0, 0))

    for tankSpawner in tankSpawners:
        screen.blit(images.get('tank1'), (tankSpawner[0] * playfield.blockSize, tankSpawner[1] * playfield.blockSize))

    screen.blit(images.get('tank3'), (playerStartLocation[0] * playfield.blockSize, playerStartLocation[1] * playfield.blockSize))

    pygame.display.flip()

def loadLevelFile(fileName):
    print(f'Loading {fileName}')
    file = open(fileName, 'rt', encoding="utf-8")
    readTankSpawnOrderFromFile(file)
    readLevelLayoutFromFile(file)
    file.close()

def readTankSpawnOrderFromFile(file):
    global tankSpawnOrder
    tankSpawnOrder = file.readline()

def readLevelLayoutFromFile(file):
    lines = file.readlines()
    for y in range(len(lines)):
        for x in range(playfield.width):
            character = lines[y][x]
            interpretLevelLayoutCharacter(character, x, y)

def interpretLevelLayoutCharacter(character, x, y):
    global baseLocation, playerStartLocation, tankSpawners

    if character == 'B':
        playfield.setTile(x, y, brickTile)
    elif character == 'C':
        playfield.setTile(x, y, concreteTile)
    elif character == '~':
        playfield.setTile(x, y, waterTile)
    elif character == '^':
        playfield.setTile(x, y, treeTile)
    elif character == 'X':
        baseLocation = (x, y)
    elif character == 'P':
        playerStartLocation = (x, y)
    elif character == 'S':
        tankSpawners.append((x, y))

def writeLevelFile(fileName):
    file = open(fileName, 'wt', encoding="utf-8")
    file.writelines([tankSpawnOrder])
    writeLevelLayoutToFile(file)
    file.close()
    print(f'Saved to {fileName}')

def writeLevelLayoutToFile(file):
    for y in range(playfield.height):
        for x in range(playfield.width):
            tankSpawner = findTankSpawnerAtTile((x, y))
            tile = playfield.getTile(x, y)

            if baseLocation == (x, y):
                file.write('X')
            elif playerStartLocation == (x, y):
                file.write('P')
            elif tankSpawner != None:
                file.write('S')
            elif tile == brickTile:
                file.write('B')
            elif tile == concreteTile:
                file.write('C')
            elif tile == waterTile:
                file.write('~')
            elif tile == treeTile:
                file.write('^')
            else:
                file.write('_')
        file.write('\n')

start()