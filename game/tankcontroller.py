import pygame
import random
import playfield
import utilities
from utilities import Timer
import pathfinder
from pathfinder import SearchGrid
import gamecontroller
from tankmover import PathProgress
from tankmover import SearchGridGenerator

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
    directions = [utilities.vectorUp, utilities.vectorRight, utilities.vectorDown, utilities.vectorLeft]
    
    def __init__(self, entity):
        self.entity = entity
        self.fireTimer = Timer(500)
        self.lastMovementTime = pygame.time.get_ticks()
        self.plannedPath = None
        self.pathPlanTime = 0
        self.planThread = None
    
    def update(self, time, timePassed):
        if self.plannedPath is None or time - self.pathPlanTime > 5000:
            self.plotPathToLocation(gamecontroller.base.location)
        else:
            self.moveAlongPath(time)

        if self.fireTimer.update(time):
            self.fire(time)

    def render(self, screen):
        if self.plannedPath != None:
            image = images.get('projectile')
            for step in self.plannedPath.path:
                screen.blit(image, (step[0] * 8, step[1] * 8))

    def moveAlongPath(self, time):
        if self.plannedPath.targetReached():
            return

        movementSteps = int((time - self.lastMovementTime ) / 50)
        if movementSteps > 0:
            for _ in range(movementSteps):
                targetStep = self.toWorldSpaceTuple(self.plannedPath.getTargetStep())
                self.moveTowardsLocation(targetStep)
                self.plannedPath.moveToNextStepIfCurrentStepIsReached(self.entity.getLocation().toIntTuple())

                if self.plannedPath.targetReached():
                    break
            self.lastMovementTime = time

    def fire(self, time):
        self.entity.fire(time)
        self.pickRandomFireTime()

    def pickRandomFireTime(self):
        self.fireTimer.setInterval(random.randint(400, 600))

    def randomDirection(self):
        return self.directions[random.randint(0, len(self.directions) - 1)]

    def plotPathToLocation(self, targetLocation):
        gridStart = pygame.time.get_ticks()
        searchGrid = SearchGridGenerator.generateSearchGridFromPlayfield()
        gridEnd =pygame.time.get_ticks()
        startPlan = pygame.time.get_ticks()
        self.plannedPath = PathProgress(searchGrid, self.toSearchSpaceCoordinateTuple(self.entity.getLocation()), self.toSearchSpaceCoordinateTuple(targetLocation))
        planEnd = pygame.time.get_ticks()
        print(f'Grid took: {gridEnd - gridStart}ms Pathfinding took {planEnd - startPlan}ms')
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
