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
        playfield.initialize(4, 4)

        self.generateSearchGridAndAssert([ \
            [0, 0], \
            [0, 0]])

    def test_generateSearchGrid_brickIsSemiPassable(self):
        playfield.initialize(4, 4)
        playfield.setTile(0, 0, Tile(TileType.BRICK))

        self.generateSearchGridAndAssert([ \
            [1, 0], \
            [0, 0]])

    def test_generateSearchGrid_waterIsImpassable(self):
        playfield.initialize(4, 4)
        playfield.setTile(0, 0, Tile(TileType.WATER))

        self.generateSearchGridAndAssert([ \
            [100, 0], \
            [0, 0]])

    def test_generateSearchGrid_treeIsPassable(self):
        playfield.initialize(4, 4)
        playfield.setTile(0, 0, Tile(TileType.TREE))

        self.generateSearchGridAndAssert([ \
            [0, 0], \
            [0, 0]])

    def test_generateSearchGrid_highestValueInQuadrantCountsTopLeft(self):
        playfield.initialize(4, 4)
        playfield.setTile(2, 2, Tile(TileType.BRICK))
        playfield.setTile(2, 3, Tile(TileType.WATER))

        self.generateSearchGridAndAssert([ \
            [0, 0], \
            [0, 100]])

    def test_generateSearchGrid_highestValueInQuadrantCountsBottomRight(self):
        playfield.initialize(4, 4)
        playfield.setTile(3, 3, Tile(TileType.BRICK))
        playfield.setTile(2, 3, Tile(TileType.WATER))

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
                self.assertEqual(expectedGrid[x][y], searchGrid.get(x, y), f'Mismatching value at {x},{y}')

if __name__ == '__main__':
    unittest.main()