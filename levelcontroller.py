import random

import images
import input
import playfield
import levels
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

def loadLevel(levelString):
    global tankSpawnLocations, upcomingTankLevels, liveEnemyTanks, base
    entities.manager.clear()
    playfield.initialize(40, 30)
    tankSpawnLocations = []
    upcomingTankLevels = [0, 1, 2, 3, 4] # , 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    liveEnemyTanks = []
    resetSpawnTimer()
    
    recreatePlayerTank()

    lines = levelString.split('\n')

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
                tankSpawnLocations.append(pixelLocation)

def recreatePlayerTank():
    global playerTank

    playerTank = entities.tank.Tank(Vector(100, 100))
    playerTank.fireTimer.setInterval(100)
    playerTank.movementSpeed = 3
    playerTankController = tankcontroller.PlayerTankController(playerTank)
    playerTank.setController(playerTankController)
    entities.manager.add(playerTank)
    input.tankController = playerTankController

def update(time, timePassed):
    pruneDeadEnemyTanks()
    spawnTankIfPossible(time)
    checkForCompletedLevel()
    endGameIfBaseIsDestroyed()

def pruneDeadEnemyTanks():
    deadTanks = []
    for tank in liveEnemyTanks:
        if tank.disposed:
            deadTanks.append(tank)

    for deadTank in deadTanks:
        liveEnemyTanks.remove(deadTank)

def checkForCompletedLevel():
    if allTanksSpawned() and not enemyTanksLeft():
        levelCompleted()

def endGameIfBaseIsDestroyed():
    if base.disposed:
        loadLevel(levels.level1)

def levelCompleted():
    loadLevel(levels.level1)

def allTanksSpawned():
    return len(upcomingTankLevels) == 0

def enemyTanksLeft():
    return len(liveEnemyTanks) > 0

def resetSpawnTimer():
    spawnTimer.setInterval(random.randint(4000, 6000))

def spawnTankIfPossible(time):
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