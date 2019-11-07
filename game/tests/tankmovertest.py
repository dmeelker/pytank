import unittest

import playfield
from tankmover import TankMover

class MockTank():
    pass

class TestTankMover(unittest.TestCase):
    def test_nothing(self):
        tank = MockTank()
        tankMover = TankMover(tank)

    def test_generateSearchSpace_empty(self):
        tank = MockTank()
        tankMover = TankMover(tank)
        game.playfield.initialize(10, 10)

        tankMover.generateSearchSpace(game.playfield)
        
if __name__ == '__main__':
    unittest.main()