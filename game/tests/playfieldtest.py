import unittest
import images
import playfield
from playfield import Tile
from playfield import TileType

class TestPlayfield(unittest.TestCase):
    def setUp(self):
        images.set('brick', None)

    def testgetTilesInPixelArea_SingleTile(self):
        setupPlayfield([\
            'BB', \
            'BB'])

        tiles = list(playfield.getTilesInPixelArea(0, 0, 8, 8))
        self.assertEqual(1, len(tiles))
        self.assertEqual(playfield.getTile(0,0), tiles[0])

    def testgetTilesInPixelArea_MultipleTilesExact(self):
        setupPlayfield([\
            'BB', \
            'BB'])

        tiles = list(playfield.getTilesInPixelArea(0, 0, 16, 16))
        self.assertEqual(4, len(tiles))
        self.assertEqual(playfield.getTile(0,0), tiles[0])
        self.assertEqual(playfield.getTile(1,0), tiles[2])
        self.assertEqual(playfield.getTile(0,1), tiles[1])
        self.assertEqual(playfield.getTile(1,1), tiles[3])

    def testgetTilesInPixelArea_MultipleTilesPartial(self):
        setupPlayfield([\
            'BB', \
            'BB'])

        tiles = list(playfield.getTilesInPixelArea(2, 2, 10, 10))
        self.assertEqual(4, len(tiles))
        self.assertEqual(playfield.getTile(0,0), tiles[0])
        self.assertEqual(playfield.getTile(1,0), tiles[2])
        self.assertEqual(playfield.getTile(0,1), tiles[1])
        self.assertEqual(playfield.getTile(1,1), tiles[3])

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