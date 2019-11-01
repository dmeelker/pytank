import entities.manager
import entities.tank
import utilities
import tankcontroller

class TankSpec:
    def __init__(self, movementSpeed, fireSpeed, hitpoints, firePower):
        self.movementSpeed = movementSpeed
        self.fireSpeed = fireSpeed
        self.hitpoints = hitpoints
        self.firePower = firePower

tankSpecs = [
    TankSpec(1, 2000, 2, 1),
    TankSpec(1, 1000, 2, 1),
    TankSpec(1, 1000, 2, 1),
    TankSpec(1, 1000, 2, 1),
    TankSpec(1, 1000, 2, 1),
    TankSpec(1, 1000, 2, 1),
    TankSpec(1, 1000, 2, 1),
    TankSpec(1, 1000, 2, 1),
    TankSpec(1, 1000, 2, 1),
    TankSpec(1, 1000, 2, 1)
]

def createTank(level, location):
    tankSpec = tankSpecs[level]

    tank = entities.tank.Tank(location)
    tank.movementSpeed = tankSpec.movementSpeed
    tank.fireTimer.setInterval(tankSpec.fireSpeed)
    tank.firePower = tankSpec.firePower
    tank.hitpoints = tankSpec.hitpoints
    tank.setHeading(utilities.vectorDown)
    tank.setController(tankcontroller.AiTankController(tank))
    entities.manager.add(tank)

    return tank