import playfield
from .pathfinder import PathFinder
from .searchgrid import SearchGrid

class PlannedPath():
    def __init__(self, searchGrid, startLocation, targetLocation):
        self.startLocation = startLocation
        self.targetLocation = targetLocation
        self.plotPath(searchGrid,startLocation, targetLocation)

    def plotPath(self, searchGrid, startLocation, targetLocation):
        pathFinder = PathFinder(searchGrid)

        self.path = pathFinder.find(startLocation, targetLocation)
        self.targetStepIndex = 1

    def moveToNextStepIfCurrentStepIsReached(self, currentLocation):
        if self.checkIfNextPathStepIsReached(currentLocation):
            if not self.targetReached():
                self.moveToNextTargetStep()
    
    def checkIfNextPathStepIsReached(self, currentLocation):
        targetLocation = self.path[self.targetStepIndex]
        targetLocation = (targetLocation[0] * 8, targetLocation[1] * 8)

        return currentLocation == targetLocation

    def moveToNextTargetStep(self):
        self.targetStepIndex += 1

    def targetReached(self):
        return self.targetStepIndex == len(self.path) - 1

    def getTarget(self):
        return self.targetLocation
    
    def getPath(self):
        return self.path

    def getTargetStepIndex(self):
        return self.targetStepIndex

    def getTargetStep(self):
        return self.path[self.targetStepIndex]
