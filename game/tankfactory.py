import utilities
import entities.tank
import tankcontroller

class TankSpec:
    def __init__(self, movementSpeed, weaponLevel, hitpoints):
        self.movementSpeed = movementSpeed
        self.weaponLevel = weaponLevel
        self.hitpoints = hitpoints

tankSpecs = [
    TankSpec(1, 1, 1),
    TankSpec(2, 1, 2),
    TankSpec(1, 1, 2),
    TankSpec(1, 3, 4),
]

def createTank(level, location):
    tankSpec = tankSpecs[level]

    tank = entities.tank.Tank(location, getGraphicsForTank(level + 1))
    tank.movementSpeed = tankSpec.movementSpeed
    tank.hitpoints = tankSpec.hitpoints
    tank.setHeading(utilities.vectorDown)
    tank.setScorePoints((level + 1) * 100)
    tank.setController(getTankController(tank))

    weapon = entities.tank.Weapon(tank, tankSpec.weaponLevel)
    weapon.setFireRateModifier(2)
    tank.setWeapon(weapon)

    return tank

def getGraphicsForTank(level):
    if level == 1:
        return entities.tank.TankGraphics.createEnemyTank2()
    elif level == 2:
        return entities.tank.TankGraphics.createEnemyTank2()
    elif level == 3:
        return entities.tank.TankGraphics.createEnemyTank1()
    elif level == 4: 
        return entities.tank.TankGraphics.createEnemyTank3()

def getTankController(tank):
    tankLevel = tank.getLevel()

    if tankLevel == 1:
        return tankcontroller.RandomMovementAiTankController(tank)
    elif tankLevel == 2:
        return tankcontroller.PlayerChargerAiTankController(tank)
    elif tankLevel == 3:
        return tankcontroller.BaseStalkerAiTankController(tank)
    elif tankLevel == 4: 
        return tankcontroller.BaseChargerAiTankController(tank)

    return tankcontroller.RandomMovementAiTankController(tank)