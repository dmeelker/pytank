import unittest

import playfield
import images
from utilities import Vector

from playfield import Tile
from playfield import TileType
from tankmover import PathProgress
from tankmover import SearchGridGenerator

class MockTank():
    def __init__(self):
        self.location = Vector(0, 0)

    def getLocation(self):
        return self.location

    def setLocation(self, location):
        self.location = location

class TestPathProgress(unittest.TestCase):
    def setUp(self):
        self.tank = MockTank()
    
    def test_setInitialization(self):
        tankMover = PathProgress((0, 0), (1, 1))
        self.assertEqual((1, 1), tankMover.getTarget())

    def test_verifyPlottedPath(self):
        setupEmptyPlayField(2, 2)
        tankMover = PathProgress((0,0), (1,0))

        self.assertEqual([(0,0), (1,0)], tankMover.getPath())
        self.assertEqual(1, tankMover.getTargetStepIndex())

    def test_checkIfNextPathStepIsReached_no(self):
        setupEmptyPlayField(2, 2)
        tankMover = PathProgress((0,0), (1,0))

        self.assertFalse(tankMover.checkIfNextPathStepIsReached((0, 0)))

    def test_checkIfNextPathStepIsReached_yes(self):
        setupEmptyPlayField(2, 2)
        tankMover = PathProgress((0,0), (1,0))

        self.assertTrue(tankMover.checkIfNextPathStepIsReached((8, 0)))

    def test_tankMovedToNextStep(self):
        setupEmptyPlayField(3, 1)
        tankMover = PathProgress((0,0), (2,0))

        tankMover.moveToNextStepIfCurrentStepIsReached((8,0))

        self.assertEqual(2, tankMover.getTargetStepIndex())

    def test_targetLocationReached(self):
        setupEmptyPlayField(2, 2)
        tankMover = PathProgress((0,0), (1,0))

        tankMover.moveToNextStepIfCurrentStepIsReached((8,0))

        self.assertTrue(tankMover.targetReached())


class TestSearchGridGenerator(unittest.TestCase):
    def setUp(self):
        images.set('brick', None)
        images.set('concrete', None)
        images.set('water', None)
        images.set('tree', None)

    def test_generateSearchGrid_initialization(self):
        playfield.initialize(5, 5)

        searchGrid = self.generateSearchGrid()
        self.assertEqual(5, searchGrid.width)
        self.assertEqual(5, searchGrid.height)

    def test_generateSearchGrid_allPassable(self):
        setupPlayfield([\
            '--', \
            '--'])

        self.generateSearchGridAndAssert([ \
            [0, 0], \
            [0, 0]])

    def test_generateSearchGrid_brickIsSemiPassable(self):
        setupPlayfield(['B'])

        self.generateSearchGridAndAssert([ \
            [1]])

    def test_generateSearchGrid_waterIsImpassable(self):
        setupPlayfield(['W'])

        self.generateSearchGridAndAssert([[100]])

    def test_generateSearchGrid_treeIsPassable(self):
        setupPlayfield(['T'])

        self.generateSearchGridAndAssert([[0]])

    def test_generateSearchGrid_horizontalGapsAreFilled(self):
        setupPlayfield([\
            '---', \
            'B-W', \
            '---'])

        self.generateSearchGridAndAssert([ \
            [0, 0, 0], \
            [1, 1, 100], \
            [0, 0, 0]])

    def test_generateSearchGrid_verticalGapsAreFilled(self):
        setupPlayfield([\
            '-B-', \
            '---', \
            '-W-'])

        self.generateSearchGridAndAssert([ \
            [0, 1, 0], \
            [0, 1, 0], \
            [0, 100, 0]])

    def generateSearchGrid(self):
        return SearchGridGenerator.generateSearchGridFromPlayfield()

    def generateSearchGridAndAssert(self, expectedGrid):
        searchGrid = self.generateSearchGrid()
        self.assertSearchGrid(searchGrid, expectedGrid)

    def assertSearchGrid(self, searchGrid, expectedGrid):
        for x in range(searchGrid.width):
            for y in range(searchGrid.height):
                self.assertEqual(expectedGrid[y][x], searchGrid.get(x, y), f'Mismatching value at {x},{y}')

def setupEmptyPlayField(width, height):
    playfield.initialize(width, height)

def setupPlayfield(data):
    height = len(data)
    width = len(data[0])
    playfield.initialize(width, height)

    for x in range(width):
        for y in range(height):
            tile = createTileFromCharacter(data[y][x])
            playfield.setTile(x, y, tile)

def createTileFromCharacter(chr):
    if chr == ' ':
        return '-'
    elif chr == 'B':
        return Tile(TileType.BRICK)
    elif chr == 'C':
        return Tile(TileType.CONCRETE)
    elif chr == 'W':
        return Tile(TileType.WATER)
    elif chr == 'T':
        return Tile(TileType.TREE)

if __name__ == '__main__':
    unittest.main()