import random
import os
import pygame

import images
import input
import playfield
import entities
import entities.tank
import entities.base
import leveldefinition

import tankfactory
import tankcontroller
import tankspawn
from powerupspawner import PowerupSpawner

import utilities
from utilities import Vector
from utilities import Timer

playerTank = None
score = 0
lives = 3

tankSpawns = []
base = None
liveEnemyTanks = []
currentLevel = 1

powerupSpawner = PowerupSpawner()
powerupTimer = Timer(40000)

overlayText = None
overlayHideTime = None

def startNewGame():
    global lives, score
    lives = 5
    score = 0
    recreatePlayerTank()
    loadLevel(1)

def loadNextLevel():
    loadLevel(currentLevel + 1)

def reloadCurrentLevel():
    recreatePlayerTank()
    loadLevel(currentLevel)

def loadLevel(levelNumber):
    global currentLevel
    resetLevelData()
    loadLevelFromFile(os.path.join('levels', f'level{levelNumber}.txt'))
    currentLevel = levelNumber
    showOverlay(f'Level {levelNumber}')

def resetLevelData():
    global tankSpawns, liveEnemyTanks

    playerTank.repair()
    entities.manager.clear()
    entities.manager.add(playerTank)
    tankSpawns = []
    liveEnemyTanks = []
    playfield.initialize(38, 28)

def loadLevelFromFile(fileName):
    level = leveldefinition.loadFromFile(fileName)

    initializeTankSpawns(level)
    initializeBaseAndPlayer(level)
    initializeMapData(level)

def initializeTankSpawns(level):
    for spawnDefinition in level.getTankSpawns():
        schedule = tankspawn.TankSpawnSchedule(pygame.time.get_ticks(), spawnDefinition.getSchedule())
        spawnLocation = convertFromTileTupleToScreenVector(spawnDefinition.getLocation())
        tankSpawns.append(tankspawn.TankSpawn(spawnLocation, schedule))

def initializeBaseAndPlayer(level):
    global base
    playerTank.setLocation(convertFromTileTupleToScreenVector(level.getPlayerSpawnLocation()))
    playerTank.setHeading(utilities.vectorUp)

    base = entities.base.Base(convertFromTileTupleToScreenVector(level.getBaseLocation()))
    entities.manager.add(base)

def initializeMapData(level):
    mapData = level.getMapData()
    for x in range(level.getSize()[0]):
        for y in range(level.getSize()[1]):
            playfield.setTile(x, y, playfield.Tile(mapData[x][y]))

def convertFromTileTupleToScreenVector(tuple):
    return Vector.fromTuple(tuple).multiplyScalar(playfield.blockSize)

def recreatePlayerTank():
    global playerTank
    playerTank = createPlayerTank()
    playerTankController = tankcontroller.PlayerTankController(playerTank)
    playerTank.setController(playerTankController)
    playerTank.setMaxHitpoints(5)

    entities.manager.add(playerTank)
    input.tankController = playerTankController

def createPlayerTank():
    tank = entities.tank.Tank(Vector(100, 100), entities.tank.TankGraphics.createPlayerTank())
    tank.movementSpeed = 1
    return tank

def update(time, timePassed):
    entities.manager.update(time, timePassed)

    spawnNewTankIfPossible(time)
    spawnPowerupIfTimerExpired(time)
    hideOverlayIfExpired(time)

    checkPlayerTankDestroyed()
    checkForCompletedLevel()
    checkForDestroyedBase()
    
def spawnPowerupIfTimerExpired(time):
    if powerupTimer.update(time):
        powerupSpawner.spawn()

def checkPlayerTankDestroyed():
    if playerTank.isDestroyed():
        reduceLivesByOne()

def checkForCompletedLevel():
    if allTanksSpawned() and not enemyTanksLeft():
        levelCompleted()

def checkForDestroyedBase():
    if base.disposed:
        reduceLivesByOne()

def levelCompleted():
    loadNextLevel()

def allTanksSpawned():
    for spawn in tankSpawns:
        if not spawn.completed():
            return False
    else:
        return True

def enemyTanksLeft():
    return len(liveEnemyTanks) > 0

def spawnNewTankIfPossible(time):
    for tankSpawn in tankSpawns:
        newTank = tankSpawn.update(time)
        if newTank != None:
            newTank.setDestroyCallback(computerTankDestroyed)
            liveEnemyTanks.append(newTank)

def destroyAllEnemyTanks():
    tanksToDestroy = liveEnemyTanks.copy()
    for tank in tanksToDestroy:
        tank.destroy()

def getBase():
    return base

def getPlayerTank():
    return playerTank

def reduceLivesByOne():
    global lives
    if lives > 0:
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

def showOverlay(text):
    global overlayText, overlayHideTime
    overlayText = text
    overlayHideTime = pygame.time.get_ticks() + 3000

def hideOverlayIfExpired(time):
    if overlayText != None and time >= overlayHideTime:
        hideOverlay()

def hideOverlay():
    global overlayText, overlayHideTime
    overlayText = None

def getScore():
    return score

def getLives():
    return lives

def getLevel():
    return currentLevel