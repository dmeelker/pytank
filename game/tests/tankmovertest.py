import unittest

import playfield
import images
from playfield import Tile
from playfield import TileType
from tankmover import TankMover
from tankmover import SearchGridGenerator



class MockTank():
    pass

class TestSearchGridGenerator(unittest.TestCase):
    def setUp(self):
        images.set('brick', None)
        images.set('concrete', None)
        images.set('water', None)
        images.set('tree', None)

    def test_generateSearchGrid_resultIsHalfSize(self):
        playfield.initialize(10, 10)

        searchGrid = self.generateSearchGrid()
        self.assertEqual(5, searchGrid.width)
        self.assertEqual(5, searchGrid.height)

    def test_generateSearchGrid_allPassable(self):
        setupPlayfield([\
            '--', \
            '--'])

        self.generateSearchGridAndAssert([[0]])

    def test_generateSearchGrid_brickIsSemiPassable(self):
        setupPlayfield([\
            'B-', \
            '--'])

        self.generateSearchGridAndAssert([[1]])

    def test_generateSearchGrid_waterIsImpassable(self):
        setupPlayfield([\
            'W-', \
            '--'])

        self.generateSearchGridAndAssert([[100]])

    def test_generateSearchGrid_treeIsPassable(self):
        setupPlayfield([\
            'T-', \
            '--'])

        self.generateSearchGridAndAssert([[0]])

    def test_generateSearchGrid_highestValueInQuadrantCountsTopLeft(self):
        setupPlayfield([\
            'BW--', \
            '----', \
            '--00', \
            '----'])

        self.generateSearchGridAndAssert([ \
            [100, 0], \
            [0, 0]])

    def test_generateSearchGrid_highestValueInQuadrantCountsBottomRight(self):
        setupPlayfield([\
            '----', \
            '----', \
            '----', \
            '--WB'])

        self.generateSearchGridAndAssert([ \
            [0, 0], \
            [0, 100]])

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