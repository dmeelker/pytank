import sys
import os
import pygame
import images
import playfield
import leveldefinition

# Pygame objects
screen = None
clock = pygame.time.Clock()
buffer = None

running = True
lastUpdateTime = 0

brickTile = None
concreteTile = None
waterTile = None
treeTile = None
activeTile = None

level = None
baseLocation = (18, 28)
tankSpawners = []
playerStartLocation = (18, 25)

openFileName = None
tankSpawnOrders = []

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
    global screen,clock,buffer
    pygame.init()
    pygame.display.set_caption("Pytank Editor")
    screen = pygame.display.set_mode((640, 480)) #, pygame.FULLSCREEN)
    buffer = pygame.surface.Surface((320, 240))
    playfield.initialize(40, 28)
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
    mouseLocation = (int(mouseLocation[0] / 2), int(mouseLocation[1] / 2))
    if pygame.mouse.get_pressed()[0]:        
        drawTileAtPixel(mouseLocation[0], mouseLocation[1], activeTile)
    if pygame.mouse.get_pressed()[2]:        
        drawTileAtPixel(mouseLocation[0], mouseLocation[1], None)

def drawTileAtPixel(x, y, tileType):
    tileX = int(x / playfield.blockSize)
    tileY = int(y / playfield.blockSize)

    if playfield.containsTileCoordinates(tileX, tileY):
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
    return (int((mouseLocation[0] / 2) / playfield.blockSize), int((mouseLocation[1] / 2) / playfield.blockSize))

def render():
    buffer.fill((0, 0, 0))

    buffer.blit(images.get('base'), (baseLocation[0] * playfield.blockSize, baseLocation[1] * playfield.blockSize))
    playfield.renderLayer(0, buffer, (0, 0))
    playfield.renderLayer(1, buffer, (0, 0))

    for tankSpawner in tankSpawners:
        buffer.blit(images.get('tank1'), (tankSpawner[0] * playfield.blockSize, tankSpawner[1] * playfield.blockSize))

    buffer.blit(images.get('tank3'), (playerStartLocation[0] * playfield.blockSize, playerStartLocation[1] * playfield.blockSize))
    drawGrid(buffer)

    pygame.transform.scale(buffer, (640, 480), screen)
    #screen.blit(buffer, (0,0))

    pygame.display.flip()

def drawGrid(surface):
    gridColor = pygame.color.Color(100, 100, 100, 20)
    for x in range(0, 20):
        pygame.draw.line(surface, gridColor, (x * 16, 0), (x * 16, 14 * 16))

    for y in range(0, 14):
        pygame.draw.line(surface, gridColor, (0, y * 16), (20 * 16, y * 16))

def loadLevelFile(fileName):
    global level
    level = leveldefinition.loadFromFile(fileName)

    initializeTankSpawns(level)
    initializeBaseAndPlayer(level)
    initializeMapData(level)

def initializeTankSpawns(level):
    for spawnDefinition in level.getTankSpawns():
        tankSpawners.append(spawnDefinition.getLocation())

def initializeBaseAndPlayer(level):
    global baseLocation, playerStartLocation

    baseLocation = level.getBaseLocation()
    playerStartLocation = level.getPlayerSpawnLocation()

def initializeMapData(level):
    mapData = level.getMapData()
    for x in range(level.getSize()[0]):
        for y in range(level.getSize()[1]):
            mapTile = mapData[x][y]
            if mapTile != None:
                
                playfield.setTile(x, y, playfield.Tile(mapTile))

def convertFromTileTupleToScreenTuple(tuple):
    return Vector.fromTuple(tuple).multiplyScalar(playfield.blockSize)

def writeLevelFile(fileName):
    file = open(fileName, 'wt', encoding="utf-8")
    file.write(f'size={level.getSize()[0]},{level.getSize()[1]}\n')
    file.write(f'spawncount={len(level.getTankSpawns())}\n')
    for spawn in level.getTankSpawns():
        file.write(spawn.getScheduleAsString())
    
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
            elif tile == None:
                file.write('_')
            elif tile.tileType == playfield.TileType.BRICK:
                file.write('B')
            elif tile.tileType == playfield.TileType.CONCRETE:
                file.write('C')
            elif tile.tileType == playfield.TileType.WATER:
                file.write('~')
            elif tile.tileType == playfield.TileType.TREE:
                file.write('^')

        file.write('\n')

start()