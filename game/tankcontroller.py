import pygame
import random
import playfield
import utilities
from utilities import Timer
#import pathfinder
#from pathfinder import SearchGrid
import gamecontroller

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
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.fire = False
    
    def update(self, time, timePassed):
        if self.moveLeft:
            self.entity.moveInDirection(utilities.vectorLeft)
        elif self.moveRight:
            self.entity.moveInDirection(utilities.vectorRight)
        if self.moveUp:
            self.entity.moveInDirection(utilities.vectorUp)
        elif self.moveDown:
            self.entity.moveInDirection(utilities.vectorDown)
        if self.fire:
            self.entity.fire(time)

class AiTankController(TankController):
    def __init__(self, entity):
        self.entity = entity
        self.fireTimer = Timer(500)
        self.lastMovementTime = pygame.time.get_ticks()
        self.plannedPath = None
        self.pathPlanTime = 0
        self.pendingSearch = None
    
    def update(self, time, timePassed):
        if self.fireTimer.update(time):
            self.fire(time)

        if self.pendingSearch != None and self.pendingSearch.isCompleted():
            if self.pendingSearch.getPath() != None:
                self.plannedPath = PlannedPath(self.pendingSearch.getPath())
                self.resetLastMovementTime(pygame.time.get_ticks())
            self.pendingSearch = None

    def render(self, screen):
        if self.plannedPath != None:
            image = images.get('projectile')
            for step in self.plannedPath.path:
                screen.blit(image, (step[0] * 8, step[1] * 8))

    def pathRecalculationNeeded(self, time):
        return time - self.pathPlanTime > 5000

    def moveAlongPath(self, time):
        movementSteps = int((time - self.lastMovementTime ) / 50)
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
        gridStart = pygame.time.get_ticks()
        searchGrid = SearchGridGenerator.generateSearchGridFromPlayfield()
        gridEnd = pygame.time.get_ticks()
        startPlan = pygame.time.get_ticks()

        start = self.toSearchSpaceCoordinateTuple(self.entity.getLocation())
        end = self.toSearchSpaceCoordinateTuple(targetLocation)
        self.pendingSearch = PathFindingTask(searchGrid, start, end)
        PathfinderWorker.queueTask(self.pendingSearch)

        self.pathPlanTime = pygame.time.get_ticks()



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

        if self.plannedPath is None or self.pathRecalculationNeeded(time):
            self.plotPathToLocation(gamecontroller.getPlayerTank().location)
        elif not self.plannedPath.targetReached():
            self.moveAlongPath(time)

class BaseChargerAiTankController(AiTankController):
    def __init__(self, entity):
        super().__init__(entity)
    
    def update(self, time, timePassed):
        super().update(time, timePassed)

        if (self.plannedPath is None and self.pendingSearch is None) or self.pathRecalculationNeeded(time):
            self.plotPathToLocation(gamecontroller.base.location)
        elif self.plannedPath != None and not self.plannedPath.targetReached():
            self.moveAlongPath(time)