import unittest

#  import game.playfield
from game.tankmover import TankMover

class MockTank():
    pass

class MockPlayField():
    def __init__(self, width, height):
        self.data = []
        self.width = width
        self.height = height

        for _ in range(width):
            column = []
            for _ in range(height):
                column.append(None)
        
            self.data.append(column)

    def getTile(self, x, y):
        return self.data[x][y]

    def setTile(self, x, y, tile):
        self.data[x][y] = tile

class TestTankMover(unittest.TestCase):
    def test_nothing(self):
        tank = MockTank()
        tankMover = TankMover(tank)

    def test_generateSearchSpace_empty(self):
        tank = MockTank()
        tankMover = TankMover(tank)
        mockPlayfield = MockPlayField(10, 10)

        tankMover.generateSearchSpace(mockPlayfield)
        
if __name__ == '__main__':
    unittest.main()