import unittest

import playfield
import images
from utilities import Vector

from playfield import Tile
from playfield import TileType
from pathfinding.plannedpath import PlannedPath
from pathfinding.searchgridgenerator import SearchGridGenerator

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
            [8]])

    def test_generateSearchGrid_waterIsImpassable(self):
        setupPlayfield(['W'])

        self.generateSearchGridAndAssert([[100]])

    def test_generateSearchGrid_treeIsPassable(self):
        setupPlayfield(['T'])

        self.generateSearchGridAndAssert([[0]])

    def test_generateSearchGrid_WallsAreThickened_Center(self):
        setupPlayfield([\
            '---', \
            '-B-', \
            '---'])

        self.generateSearchGridAndAssert([ \
            [0, 8, 0], \
            [8, 8, 0], \
            [0, 0, 0]])

    def test_generateSearchGrid_WallsAreThickened_LeftEdge(self):
        setupPlayfield([\
            '---', \
            'B--', \
            '---'])

        self.generateSearchGridAndAssert([ \
            [8, 0, 0], \
            [8, 0, 0], \
            [0, 0, 0]])

    def test_generateSearchGrid_WallsAreThickened_TopEdge(self):
        setupPlayfield([\
            '-B-', \
            '---', \
            '---'])

        self.generateSearchGridAndAssert([ \
            [8, 8, 0], \
            [0, 0, 0], \
            [0, 0, 0]])

    def test_generateSearchGrid_randomShape(self):
        setupPlayfield([\
            '-W-T', \
            '-W-C', \
            '----', \
            'BBBB'])

        self.generateSearchGridAndAssert([ \
            [100, 100, 0, 100], \
            [100, 100, 100, 100], \
            [8, 8, 8, 8], \
            [8, 8, 8, 8]])

    def generateSearchGrid(self):
        return SearchGridGenerator.generateSearchGridFromPlayfield()

    def generateSearchGridAndAssert(self, expectedGrid):
        searchGrid = self.generateSearchGrid()
        self.assertSearchGrid(searchGrid, expectedGrid)

    def assertSearchGrid(self, searchGrid, expectedGrid):
        for x in range(searchGrid.width):
            for y in range(searchGrid.height):
                self.assertEqual(expectedGrid[y][x], searchGrid.get(x, y), f'Mismatching value at {x},{y}')

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