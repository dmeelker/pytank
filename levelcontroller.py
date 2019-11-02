import images
import input
import playfield
import levels
import entities
import entities.tank
import entities.base
import tankcontroller
from tankspawner import TankSpawner

import utilities
from utilities import Vector

tankSpawners = []
base = None
playerTank = None

def loadLevel(levelString):
    global tankSpawners, base, playerTank
    entities.manager.clear()
    playfield.initialize(40, 30)
    
    playerTank = entities.tank.Tank(Vector(100, 100))
    playerTank.fireTimer.setInterval(100)
    playerTank.movementSpeed = 3
    playerTankController = tankcontroller.PlayerTankController(playerTank)
    playerTank.setController(playerTankController)
    entities.manager.add(playerTank)
    input.tankController = playerTankController

    lines = levelString.split('\n')
    tankSpawners = []

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
                tankSpawners.append(TankSpawner(pixelLocation))

def update(time, timePassed):
    updateTankSpawners(time, timePassed)

    
    if base.disposed:
        loadLevel(levels.level1)

def updateTankSpawners(time, timePassed):
    for tankSpawner in tankSpawners:
        tankSpawner.update(time, timePassed)
