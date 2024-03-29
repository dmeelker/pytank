import pygame
import random
import playfield
import utilities
from utilities import Timer

import gamecontroller
import input

from pathfinding.plannedpath import PlannedPath
from pathfinding.searchgridgenerator import SearchGridGenerator
from pathfinding.searchgrid import SearchGrid
import pathfinding.pathfindingbackgroundworker as PathfinderWorker
from pathfinding.pathfindingbackgroundworker import Task as PathFindingTask

import images

class TankController:
    def update(self, time, timePassed):
        pass

    def render(self, screen):
        pass

class PlayerTankController(TankController):
    def __init__(self, entity):
        self.entity = entity
    
    def update(self, time, timePassed):
        if input.buttonStates.left:
            self.entity.moveInDirection(utilities.vectorLeft)
        elif input.buttonStates.right:
            self.entity.moveInDirection(utilities.vectorRight)
        if input.buttonStates.up:
            self.entity.moveInDirection(utilities.vectorUp)
        elif input.buttonStates.down:
            self.entity.moveInDirection(utilities.vectorDown)
        if input.buttonStates.fire:
            self.entity.fire(time)

class AiTankController(TankController):
    def __init__(self, entity):
        self.entity = entity
        self.fireTimer = Timer(500)
        self.lastMovementTime = pygame.time.get_ticks()
        self.pendingPathSearch = None
        self.plannedPath = None
        self.pathPlanTime = 0
        self.searchGridFunction = SearchGridGenerator.getSearchSpaceCellValueForTile
        self.stepLength = 50
    
    def update(self, time, timePassed):
        if self.fireTimer.update(time):
            self.fire(time)

        if self.isPathPlanningPending() and self.isPathPlanningCompleted():
            if self.pendingPathSearch.pathFound():
                self.plannedPath = PlannedPath(self.pendingPathSearch.getPath())
                self.resetLastMovementTime(pygame.time.get_ticks())
            self.pendingPathSearch = None

    def render(self, screen):
        pass
        #self.renderPlannedPath(screen)

    def renderPlannedPath(self, screen):
        if self.plannedPath != None:
            image = images.get('projectile')
            for step in self.plannedPath.path:
                screen.blit(image, ((step[0] * 8) + 8, step[1] * 8))

    def pathRecalculationNeeded(self, time):
        return (not self.hasPath() and not self.isPathPlanningPending()) or self.isPlannedPathExpired(time)

    def isPlannedPathExpired(self, time):
        return time - self.pathPlanTime > 5000

    def canMoveAlongPath(self):
        return self.hasPath() and not self.plannedPath.targetReached()

    def moveAlongPath(self, time):
        movementSteps = int((time - self.lastMovementTime ) / self.stepLength)
        if movementSteps > 0:
            for _ in range(movementSteps):
                self.stepTowardsTarget()
                if self.plannedPath.targetReached():
                    break
            self.resetLastMovementTime(time)

    def resetLastMovementTime(self, time):
        self.lastMovementTime = time

    def stepTowardsTarget(self):
        targetStep = self.toWorldSpaceTuple(self.plannedPath.getTargetStep())
        self.moveTowardsLocation(targetStep)
        self.plannedPath.moveToNextStepIfCurrentStepIsReached(self.entity.getLocation().toIntTuple())

    def fire(self, time):
        self.entity.fire(time)
        self.pickRandomFireTime()

    def pickRandomFireTime(self):
        self.fireTimer.setInterval(random.randint(400, 600))

    def plotPathToLocation(self, targetLocation):
        searchGrid = SearchGridGenerator.generateSearchGridFromPlayfield(self.searchGridFunction)
        start = self.toSearchSpaceCoordinateTuple(self.entity.getLocation())
        end = self.toSearchSpaceCoordinateTuple(targetLocation)
        
        self.pendingPathSearch = PathFindingTask(searchGrid, start, end)
        PathfinderWorker.queueTask(self.pendingPathSearch)

        self.pathPlanTime = pygame.time.get_ticks()

    def isPathPlanningPending(self):
        return self.pendingPathSearch != None

    def isPathPlanningCompleted(self):
        return self.pendingPathSearch != None and self.pendingPathSearch.isCompleted()

    def hasPath(self):
        return self.plannedPath != None

    def moveTowardsLocation(self, targetLocation):
        location = self.entity.location
        if location.x < targetLocation[0]:
            self.entity.moveSingleStep(utilities.vectorRight)
        elif location.x > targetLocation[0]:
            self.entity.moveSingleStep(utilities.vectorLeft)
        elif location.y < targetLocation[1]:
            self.entity.moveSingleStep(utilities.vectorDown)
        elif location.y > targetLocation[1]:
            self.entity.moveSingleStep(utilities.vectorUp)

    def toSearchSpaceCoordinateTuple(self, coordinates):
        return (int(coordinates.x / 8), int(coordinates.y / 8))

    def toWorldSpaceTuple(self, coordinates):
        return (int(coordinates[0] * 8), int(coordinates[1] * 8))

class RandomMovementAiTankController(AiTankController):
    directions = [utilities.vectorUp, utilities.vectorRight, utilities.vectorDown, utilities.vectorLeft]

    def __init__(self, entity):
        super().__init__(entity)
    
    def update(self, time, timePassed):
        super().update(time, timePassed)
        
        self.move(time)

        if self.fireTimer.update(time):
            self.fire(time)

    def move(self, time):
        movementSteps = int((time - self.lastMovementTime ) / 50)
        if movementSteps > 0:
            for _ in range(movementSteps):
                self.step()
            self.lastMovementTime = time

    def step(self):
        heading = self.entity.getHeading()

        if random.randint(0, 1000) < 5:
            heading = self.randomFreeDirection()

        if not self.entity.canMoveInDirection(heading):
            heading = self.randomFreeDirection()

        self.entity.moveSingleStep(heading)   

    def randomFreeDirection(self):
        for _ in range(5):
            direction = self.randomDirection()
            if self.entity.canMoveInDirection(direction):
                return direction
        else:
            return utilities.vectorDown

    def randomDirection(self):
        return self.directions[random.randint(0, len(self.directions) - 1)]

class PlayerChargerAiTankController(AiTankController):
    def __init__(self, entity):
        super().__init__(entity)
    
    def update(self, time, timePassed):
        super().update(time, timePassed)

        if self.pathRecalculationNeeded(time):
            self.plotPathToLocation(gamecontroller.getPlayerTank().location)
        elif self.canMoveAlongPath():
            self.moveAlongPath(time)

class BaseChargerAiTankController(AiTankController):
    def __init__(self, entity):
        super().__init__(entity)
        self.stepLength = 100
        self.searchGridFunction = BaseChargerAiTankController.getSearchSpaceCellValueForTile
    
    def update(self, time, timePassed):
        super().update(time, timePassed)

        if self.pathRecalculationNeeded(time):
            self.plotPathToLocation(gamecontroller.base.location)
        elif self.canMoveAlongPath():
            self.moveAlongPath(time)

    @staticmethod
    def getSearchSpaceCellValueForTile(tile):
        if tile is None:
            return 0
        elif tile.tileType == playfield.TileType.BRICK:
            return 0
        else:
            return SearchGridGenerator.getSearchSpaceCellValueForTile(tile)

class BaseStalkerAiTankController(AiTankController):
    def __init__(self, entity):
        super().__init__(entity)
    
    def update(self, time, timePassed):
        super().update(time, timePassed)

        if self.pathRecalculationNeeded(time):
            self.plotPathToLocation(gamecontroller.base.location)
        elif self.canMoveAlongPath():
            self.moveAlongPath(time)