import unittest

import leveldefinition
import playfield

basicLevel = 'size=5,2\n\
spawncount=2\n\
0:0 1:1\n\
1:1 2:2\n\
~S^S_\n\
BXCP_'

class TestLevelDefinition(unittest.TestCase):
    def test_sizeMatches(self):
        level = leveldefinition.loadFromString(basicLevel)
        self.assertEqual((5,2), level.getSize())

    def test_mapDataSizeMatches(self):
        level = leveldefinition.loadFromString(basicLevel)
        mapData = level.getMapData()
        self.assertEqual(5, len(mapData))
        self.assertEqual(2, len(mapData[0]))

    def test_spawnCountMatches(self):
        level = leveldefinition.loadFromString(basicLevel)
        self.assertEqual(2, len(level.getTankSpawns()))

    def test_spawnScheduleMatches(self):
        level = leveldefinition.loadFromString(basicLevel)

        spawn1 = level.getTankSpawns()[0]
        self.assertEqual([(0,0), (1,1)], spawn1.getSchedule())

        spawn2 = level.getTankSpawns()[1]
        self.assertEqual([(1,1), (2,2)], spawn2.getSchedule())
        
    def test_tankSpawnLocations(self):
        level = leveldefinition.loadFromString(basicLevel)
        
        spawn1 = level.getTankSpawns()[0]
        self.assertEqual((1,0), spawn1.getLocation())

        spawn2 = level.getTankSpawns()[1]
        self.assertEqual((3,0), spawn2.getLocation())

    def test_baseLocation(self):
        level = leveldefinition.loadFromString(basicLevel)
        self.assertEqual((1,1), level.getBaseLocation())

    def test_playerLocation(self):
        level = leveldefinition.loadFromString(basicLevel)
        self.assertEqual((3,1), level.getPlayerSpawnLocation())

    def test_mapData(self):
        level = leveldefinition.loadFromString(basicLevel)

        self.assertMapData([\
            [playfield.TileType.WATER, None, playfield.TileType.TREE, None, None], \
            [playfield.TileType.BRICK, None, playfield.TileType.CONCRETE, None, None]], level.getMapData())

    def assertMapData(self, expectedTiles, mapData):
        for x in range(len(mapData)):
            for y in range(len(mapData[0])):
                self.assertEqual(expectedTiles[y][x], mapData[x][y])

