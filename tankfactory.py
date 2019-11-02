import utilities
import entities.tank
import tankcontroller

class TankSpec:
    def __init__(self, movementSpeed, fireSpeed, hitpoints, firePower):
        self.movementSpeed = movementSpeed
        self.fireSpeed = fireSpeed
        self.hitpoints = hitpoints
        self.firePower = firePower

tankSpecs = [
    TankSpec(1, 2000, 1, 1),
    TankSpec(2, 2000, 2, 1),
    TankSpec(1, 3000, 4, 2),
    # TankSpec(1, 1000, 2, 1),
    # TankSpec(1, 1000, 2, 1),
    # TankSpec(1, 1000, 2, 1),
    # TankSpec(1, 1000, 2, 1),
    # TankSpec(1, 1000, 2, 1),
    # TankSpec(1, 1000, 2, 1),
    # TankSpec(1, 1000, 2, 1)
]

def createTank(level, location):
    tankSpec = tankSpecs[level]

    tank = entities.tank.Tank(location, level + 1)
    tank.movementSpeed = tankSpec.movementSpeed
    tank.fireTimer.setInterval(tankSpec.fireSpeed)
    tank.firePower = tankSpec.firePower
    tank.hitpoints = tankSpec.hitpoints
    tank.setHeading(utilities.vectorDown)
    tank.setController(tankcontroller.AiTankController(tank))

    return tank