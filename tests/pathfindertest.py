import unittest

from game.pathfinder import PathFinder

class TestStringMethods(unittest.TestCase):

    def test_freePath(self):
        pathFinder = PathFinder([\
            [0, 0]])

        foundPath = pathFinder.find((0,0), (1,1))
        
        self.assertEqual([(0,0), (1,1)], foundPath)

    def test_directPathBlockedByImpenetrable(self):
        pathFinder = PathFinder([\
            [0, 0, 0], \
            [0, -1, 0], \
            [0, -1, 0]])
        foundPath = pathFinder.find((0,1), (2,1))
        
        self.assertEqual([(0,1), (0,0), (1,0), (2,0), (2,1)], foundPath)


if __name__ == '__main__':
    unittest.main()