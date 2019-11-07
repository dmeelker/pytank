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

playerTank = None
score = 0
lives = 3

tankSpawnLocations = []
upcomingTankLevels = []
base = None
liveEnemyTanks = []
spawnTimer = Timer(5000)
currentLevel = 1

def initialize():
    pass

def startNewGame():
    global lives, score
    lives = 3
    score = 0
    recreatePlayerTank()
    loadLevel(1)

def loadNextLevel():
    loadLevel(currentLevel + 1)

def reloadCurrentLevel():
    loadLevel(currentLevel)

def loadLevel(levelNumber):
    global currentLevel
    resetLevelData()
    loadLevelFromFile(os.path.join('levels', f'level{levelNumber}.txt'))
    currentLevel = levelNumber

def resetLevelData():
    global tankSpawnLocations, upcomingTankLevels, liveEnemyTanks
    entities.manager.clear()
    entities.manager.add(playerTank)
    tankSpawnLocations = []
    upcomingTankLevels = []
    liveEnemyTanks = []
    playfield.initialize(40, 30)
    resetSpawnTimer()

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
        playfield.setTile(x, y, playfield.Tile(playfield.TileType.BRICK))
    elif character == 'C':
        playfield.setTile(x, y, playfield.Tile(playfield.TileType.CONCRETE))
    elif character == '~':
        playfield.setTile(x, y, playfield.Tile(playfield.TileType.WATER))
    elif character == '^':
        playfield.setTile(x, y, playfield.Tile(playfield.TileType.TREE))
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
    playerTank.setDestroyCallback(playerTankDestroyed)

    entities.manager.add(playerTank)
    input.tankController = playerTankController

def createPlayerTank():
    tank = entities.tank.Tank(Vector(100, 100), type=1)
    tank.movementSpeed = 3
    return tank

def update(time, timePassed):
    spawnNewTankIfPossible(time)
    checkForCompletedLevel()
    checkForDestroyedBase()
    
def checkForCompletedLevel():
    if allTanksSpawned() and not enemyTanksLeft():
        levelCompleted()

def checkForDestroyedBase():
    if base.disposed:
        reduceLivesByOne()

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
    tank.setDestroyCallback(computerTankDestroyed)
    liveEnemyTanks.append(tank)
    entities.manager.add(tank)

def getRandomTankSpawnLocation():
    return tankSpawnLocations[random.randint(0, len(tankSpawnLocations) -1)] 

def playerTankDestroyed(tank):
    reduceLivesByOne()

def reduceLivesByOne():
    global lives
    if lives > 1:
        lives -= 1
        reloadCurrentLevel()
        print(f'Lost a live, {lives} lives left')
    else:
        endGame()

def endGame():
    print(f'Game ended! Final score {score}')
    startNewGame()

def computerTankDestroyed(tank):
    removeTankFromLiveList(tank)
    addScorePoints(tank.getScorePoints())

def removeTankFromLiveList(tank):
    liveEnemyTanks.remove(tank)

def addScorePoints(points):
    global score
    score += points
    print(f'New score: {score}')