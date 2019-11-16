import entities.manager
import tankfactory

class TankSpawn():
    def __init__(self, location, schedule):
        self.location = location
        self.schedule = schedule

    def update(self, time):
        tankType = self.schedule.getTankToSpawn(time)

        if tankType != None:
            return self.spawnTank(tankType)
        else:
            return None

    def spawnTank(self, tankType):
        print(f'Spawning tank of level {tankType}')
        tank = tankfactory.createTank(tankType, self.location)
        entities.manager.add(tank)
        return tank

    def setLocation(self, location):
        self.location = location

    def completed(self):
        return self.schedule.completed()

class TankSpawnSchedule():
    def __init__(self, creationTime, spawnMoments):
        self.creationTime = creationTime
        self.spawnMoments = spawnMoments

    def getTimeSinceInitialization(self, time):
        return time - self.creationTime

    def getTankToSpawn(self, time):
        timeSinceCreation = time - self.creationTime

        if len(self.spawnMoments) == 0:
            return None

        nextSpawnMoment = self.spawnMoments[0]
        if nextSpawnMoment[0] <= timeSinceCreation:
            self.spawnMoments.remove(nextSpawnMoment)
            return nextSpawnMoment[1]
        else:
            return None

    def getSpawnMoments(self):
        return self.spawnMoments

    def completed(self):
        return len(self.spawnMoments) == 0

    @staticmethod
    def parseSpawnMomentsFromString(input):
        spawnMoments = []
        parts = input.split(' ')

        for partString in parts:
            partString = partString.strip()
            if len(partString) == 0:
                continue

            components = partString.split(':')
            time = int(components[0])
            tankType = int(components[1])
            spawnMoments.append((time * 1000, tankType))
        return spawnMoments

