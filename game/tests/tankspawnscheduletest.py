import unittest
import tankspawnschedule

class TestTankSpawnSchedule(unittest.TestCase):
    def test_getTimeSinceInitialization(self):
        spawner = tankspawnschedule.TankSpawnSchedule(0, [(0,0)])
        self.assertEqual(100, spawner.getTimeSinceInitialization(100))

    def test_noTankToSpawn(self):
        spawner = tankspawnschedule.TankSpawnSchedule(1000, [(0,0), (100,0)])
        self.assertIsNone(spawner.getTankToSpawn(0))

    def test_singleTankToSpawn(self):
        spawner = tankspawnschedule.TankSpawnSchedule(0, [(0,0)])
        self.assertEqual(0, spawner.getTankToSpawn(0))
        self.assertIsNone(spawner.getTankToSpawn(1))

    def test_range(self):
        spawner = tankspawnschedule.TankSpawnSchedule(0, [(0,0), (100,1)])
        self.assertEqual(0, spawner.getTankToSpawn(0))
        self.assertEqual(1, spawner.getTankToSpawn(101))
        self.assertIsNone(spawner.getTankToSpawn(102))

    def test_parseSpawnMomentsFromString(self):
        schedule = tankspawnschedule.TankSpawnSchedule.parseSpawnMomentsFromString('0:0 1:1 2:2')
        self.assertEqual([(0,0), (1000,1), (2000, 2)], schedule)

    def test_parseSpawnMomentsFromStringWhitespace(self):
        schedule = tankspawnschedule.TankSpawnSchedule.parseSpawnMomentsFromString('     0:0       1:1 2:2   ')
        self.assertEqual([(0,0), (1000,1), (2000, 2)], schedule)