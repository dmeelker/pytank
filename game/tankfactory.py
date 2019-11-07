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
    tank.setController(getTankController(tank))

    return tank

def getTankController(tank):
    tankLevel = tank.getLevel()

    if tankLevel == 1:
        return tankcontroller.RandomMovementAiTankController(tank)
    elif tankLevel == 2:
        return tankcontroller.PlayerChargerAiTankController(tank)
    elif tankLevel == 3:
        return tankcontroller.BaseChargerAiTankController(tank)

    return tankcontroller.RandomMovementAiTankController(tank)