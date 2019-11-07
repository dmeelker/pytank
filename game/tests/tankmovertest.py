import unittest

import playfield
import images
from utilities import Vector

from playfield import Tile
from playfield import TileType
from tankmover import PlannedPath
from tankmover import SearchGridGenerator

class MockTank():
    def __init__(self):
        self.location = Vector(0, 0)

    def getLocation(self):
        return self.location

    def setLocation(self, location):
        self.location = location

class TestPlannedPath(unittest.TestCase):
    def setUp(self):
        self.tank = MockTank()
    
    def test_setInitialization(self):
        path = self.createPath((0, 0), (1, 1))
        self.assertEqual((1, 1), path.getTarget())

    def test_verifyPlottedPath(self):
        setupEmptyPlayField(2, 2)
        path = self.createPath((0,0), (1,0))

        self.assertEqual([(0,0), (1,0)], path.getPath())
        self.assertEqual(1, path.getTargetStepIndex())

    def test_checkIfNextPathStepIsReached_no(self):
        setupEmptyPlayField(2, 2)
        path = self.createPath((0,0), (1,0))

        self.assertFalse(path.checkIfNextPathStepIsReached((0, 0)))

    def test_checkIfNextPathStepIsReached_yes(self):
        setupEmptyPlayField(2, 2)
        path = self.createPath((0,0), (1,0))

        self.assertTrue(path.checkIfNextPathStepIsReached((8, 0)))

    def test_tankMovedToNextStep(self):
        setupEmptyPlayField(3, 1)
        path = self.createPath((0,0), (2,0))

        path.moveToNextStepIfCurrentStepIsReached((8,0))

        self.assertEqual(2, path.getTargetStepIndex())

    def test_targetLocationReached(self):
        setupEmptyPlayField(2, 2)
        path = self.createPath((0,0), (1,0))

        path.moveToNextStepIfCurrentStepIsReached((8,0))

        self.assertTrue(path.targetReached())

    def createPath(self, startLocation, endLocation):
        searchGrid = SearchGridGenerator.generateSearchGridFromPlayfield()
        return PlannedPath(searchGrid, startLocation, endLocation)

def setupEmptyPlayField(width, height):
    playfield.initialize(width, height)

if __name__ == '__main__':
    unittest.main()