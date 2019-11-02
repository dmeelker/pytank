import random
import os

import images
import input
import playfield
import entities
import entities.tank
import entities.base
import tankfactory
import tankcontroller

import utilities
from utilities import Vector
from utilities import Timer

tankSpawnLocations = []
upcomingTankLevels = []
base = None
playerTank = None
liveEnemyTanks = []
spawnTimer = Timer(5000)
currentLevel = 1

def loadFirstLevel():
    loadLevel(1)

def loadNextLevel():
    loadLevel(currentLevel + 1)

def loadLevel(levelNumber):
    global currentLevel
    resetGame()
    loadLevelFromFile(os.path.join('levels', f'level{levelNumber}.txt'))
    currentLevel = levelNumber

def resetGame():
    global tankSpawnLocations, upcomingTankLevels, liveEnemyTanks
    entities.manager.clear()
    tankSpawnLocations = []
    upcomingTankLevels = []
    liveEnemyTanks = []
    playfield.initialize()
    resetSpawnTimer()
    
    recreatePlayerTank()

def loadLevelFromFile(fileName):
    file = open(fileName, 'rt', encoding="utf-8")
    readTankSpawnOrderFromFile(file)
    readLevelLayoutFromFile(file)
    file.close()

def readTankSpawnOrderFromFile(file):
    global upcomingTankLevels
    spawnOrderLine = file.readline()
    tankLevelsAsString = spawnOrderLine.split(' ')
    for levelString in tankLevelsAsString:
        upcomingTankLevels.append(int(levelString))

def readLevelLayoutFromFile(file):
    lines = file.readlines()
    for y in range(len(lines)):
        for x in range(playfield.width):
            character = lines[y][x]
            interpretLevelLayoutCharacter(character, x, y)

def interpretLevelLayoutCharacter(character, x, y):
    global tankSpawnLocations, base
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
        tankSpawnLocations.append(pixelLocation)

def recreatePlayerTank():
    global playerTank
    playerTank = createPlayerTank()
    playerTankController = tankcontroller.PlayerTankController(playerTank)
    playerTank.setController(playerTankController)
    playerTank.hitpoints = 5

    entities.manager.add(playerTank)
    input.tankController = playerTankController

def createPlayerTank():
    tank = entities.tank.Tank(Vector(100, 100), type=1)
    tank.fireTimer.setInterval(1000)
    tank.movementSpeed = 1
    return tank

def update(time, timePassed):
    pruneDeadEnemyTanks()
    spawnNewTankIfPossible(time)
    checkForCompletedLevel()
    endGameIfBaseIsDestroyed()

def pruneDeadEnemyTanks():
    disposedTanks = getDisposedTanks()

    for disposedTank in disposedTanks:
        liveEnemyTanks.remove(disposedTank)

def getDisposedTanks():
    disposedTanks = []
    for tank in liveEnemyTanks:
        if tank.disposed:
            disposedTanks.append(tank)
    return disposedTanks
    
def checkForCompletedLevel():
    if allTanksSpawned() and not enemyTanksLeft():
        levelCompleted()

def endGameIfBaseIsDestroyed():
    if base.disposed:
        loadFirstLevel()

def levelCompleted():
    loadNextLevel()

def allTanksSpawned():
    return len(upcomingTankLevels) == 0

def enemyTanksLeft():
    return len(liveEnemyTanks) > 0

def resetSpawnTimer():
    spawnTimer.setInterval(random.randint(4000, 6000))

def spawnNewTankIfPossible(time):
    if not allTanksSpawned() and spawnTimer.update(time):
        spawnTank()

def spawnTank():
    location = getRandomTankSpawnLocation()
    tankLevel = upcomingTankLevels.pop(0)
    print(f'Spawning tank of level {tankLevel}')
    tank = tankfactory.createTank(tankLevel, location)

    liveEnemyTanks.append(tank)
    entities.manager.add(tank)

def getRandomTankSpawnLocation():
    return tankSpawnLocations[random.randint(0, len(tankSpawnLocations) -1)]