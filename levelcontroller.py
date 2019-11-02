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
base = None
playerTank = None

spawnTimer = Timer(5000)

def loadLevel(levelString):
    global tankSpawnLocations, base, playerTank
    entities.manager.clear()
    playfield.initialize(40, 30)
    resetSpawnTimer()
    
    playerTank = entities.tank.Tank(Vector(100, 100))
    playerTank.fireTimer.setInterval(100)
    playerTank.movementSpeed = 3
    playerTankController = tankcontroller.PlayerTankController(playerTank)
    playerTank.setController(playerTankController)
    entities.manager.add(playerTank)
    input.tankController = playerTankController

    lines = levelString.split('\n')
    tankSpawnLocations = []

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

def update(time, timePassed):
    if spawnTimer.update(time):
        spawnTank()
    
    if base.disposed:
        loadLevel(levels.level1)

def resetSpawnTimer():
    spawnTimer.setInterval(random.randint(4000, 6000))

def spawnTank():
    location = getRandomTankSpawnLocation()
    tank = tankfactory.createTank(0, location)
    entities.manager.add(tank)

def getRandomTankSpawnLocation():
    return tankSpawnLocations[random.randint(0, len(tankSpawnLocations) -1)]