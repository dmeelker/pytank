import utilities
import entities.tank
import tankcontroller

class TankSpec:
    def __init__(self, movementSpeed, weaponLevel, hitpoints, firePower):
        self.movementSpeed = movementSpeed
        self.weaponLevel = weaponLevel
        self.hitpoints = hitpoints
        self.firePower = firePower

tankSpecs = [
    TankSpec(1, 1, 1, 1),
    TankSpec(2, 1, 2, 1),
    TankSpec(1, 1, 4, 2),
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
    tank.setWeapon(entities.tank.Weapon(tank, tankSpec.weaponLevel))
    tank.movementSpeed = tankSpec.movementSpeed
    tank.hitpoints = tankSpec.hitpoints
    tank.setHeading(utilities.vectorDown)
    tank.setController(tankcontroller.AiTankController(tank))

    return tank