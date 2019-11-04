import unittest

from game.pathfinder import PriorityQueue
from game.pathfinder import SearchGrid
from game.pathfinder import PathFinder

INPENETRABLE = -1
EXTRACOST = 1

class TestPathFinder(unittest.TestCase):
    def test_startLocationIsSameAsEndLocation(self):
        pathFinder = PathFinder(SearchGrid(5, 5))

        foundPath = pathFinder.find((0,0), (0,0))
        
        self.assertEqual([(0,0)], foundPath)

    def test_freePath(self):
        pathFinder = PathFinder(SearchGrid(5, 5))

        foundPath = pathFinder.find((0,0), (1,0))
        
        self.assertEqual([(0,0), (1,0)], foundPath)

    def test_directPathBlockedByImpenetrable(self):
        grid = SearchGrid(5, 5)
        grid.set(1, 0, INPENETRABLE)
        pathFinder = PathFinder(grid)

        foundPath = pathFinder.find((0,0), (2,0))
        self.assertEqual([(0,0), (0,1), (1,1), (2,1), (2,0)], foundPath)

    def test_noPath(self):
        grid = SearchGrid(3, 1)
        grid.set(1, 0, INPENETRABLE)
        pathFinder = PathFinder(grid)

        foundPath = pathFinder.find((0,0), (2,0))
        self.assertEqual(None, foundPath)

    def test_shortestPathGoesOverExtraCostCell(self):
        grid = SearchGrid(5, 5)
        grid.set(1, 0, EXTRACOST)
        grid.set(1, 1, INPENETRABLE)

        pathFinder = PathFinder(grid)

        foundPath = pathFinder.find((0,0), (2,0))
        
        self.assertEqual([(0,0), (1,0), (2,0)], foundPath)

class TestPriorityQueue(unittest.TestCase):
    def test_emptyQueue(self):
        self.assertTrue(PriorityQueue().isEmpty())

    def test_singleValue(self):
        queue = PriorityQueue()
        queue.insert((1, 'Monkey'))

        smallestValue = queue.getSmallest()
        self.assertEqual(1, smallestValue[0])

    def test_multipleValues(self):
        queue = PriorityQueue()
        queue.insert((10, 'Item 10'))
        queue.insert((1, 'Item 1'))
        queue.insert((5, 'Item 5'))

        self.assertEqual(1, queue.getSmallest()[0])
        self.assertEqual(5, queue.getSmallest()[0])
        self.assertEqual(10, queue.getSmallest()[0])

class TestSearchGrid(unittest.TestCase):
    def test_sizeIsSet(self):
        grid = SearchGrid(5, 5)

        self.assertEqual(5, grid.width)
        self.assertEqual(5, grid.height)

    def test_cellsAreZeroUponInitialization(self):
        grid = SearchGrid(5, 5)

        for x in range(grid.width):
            for y in range(grid.height):
                self.assertEqual(0, grid.get(x, y))

    def test_set(self):
        grid = SearchGrid(5, 5)
        grid.set(1, 1, 10)
        self.assertEqual(10, grid.get(1, 1))

    def test_containsCoordinatesOutOfBounds(self):
        grid = SearchGrid(5, 5)
        self.assertFalse(grid.containsCoordinates(-1, 0))
        self.assertFalse(grid.containsCoordinates(0, -1))
        self.assertFalse(grid.containsCoordinates(5, 0))
        self.assertFalse(grid.containsCoordinates(0, 5))

    def test_containsCoordinatesInsideBounds(self):
        grid = SearchGrid(5, 5)
        self.assertTrue(grid.containsCoordinates(0, 0))
        self.assertTrue(grid.containsCoordinates(4, 4))

    def test_getAdjacentCellCoordinatesMiddle(self):
        grid = SearchGrid(5, 5)
        result = grid.getAdjacentCellCoordinates(1, 1)
        self.assertEqual(4, len(result))
        self.assertTrue((0, 1) in result)
        self.assertTrue((2, 1) in result)
        self.assertTrue((1, 0) in result)
        self.assertTrue((1, 2) in result)

    def test_getAdjacentCellCoordinatesTopLeft(self):
        grid = SearchGrid(5, 5)
        result = grid.getAdjacentCellCoordinates(0, 0)
        self.assertEqual(2, len(result))
        self.assertTrue((1, 0) in result)
        self.assertTrue((0, 1) in result)

    def test_getAdjacentCellCoordinatesBottomRight(self):
        grid = SearchGrid(5, 5)
        result = grid.getAdjacentCellCoordinates(4, 4)
        self.assertEqual(2, len(result))
        self.assertTrue((4, 3) in result)
        self.assertTrue((3, 4) in result)


if __name__ == '__main__':
    unittest.main()