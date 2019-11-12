import enum
import images

blockSize = 8
tiles = []
width = 0
height = 0
pixelWidth = 0
pixelHeight = 0

def initialize(w, h):
    global width, height, pixelWidth, pixelHeight, tiles
    tiles = []
    width = w
    height = h
    pixelWidth = w * blockSize
    pixelHeight = h * blockSize

    for _ in range(width):
        column = []
        for _ in range(height):
            column.append(None)
        
        tiles.append(column)

def setTile(x, y, tile):
    tiles[x][y] = tile

def getTile(x, y):
    return tiles[x][y]

def getTilesInQuad(x, y):
    return [tiles[x][y], tiles[x+1][y], tiles[x][y+1], tiles[x+1][y+1]]

def getTileAtPixel(x, y):
    tileX = int(x / blockSize)
    tileY = int(y / blockSize)

    if not containsTileCoordinates(tileX, tileY):
        return None

    return tiles[tileX][tileY]

def convertPixelToTileCoordinates(pixelCoordinates):
    # + 80 - 10 to make this work with negative coordinates too
    return (int((pixelCoordinates[0] + 80) / blockSize) - 10, int((pixelCoordinates[1] + 80) / blockSize) - 10)

def containsTileCoordinates(x, y):
    return not (x < 0 or x >= width or y < 0 or y >= height)

def containsPixelCoordinates(x, y):
    return not (x < 0 or x >= pixelWidth or y < 0 or y >= pixelHeight)

def renderLayer(layer, screen, offset):
    for x in range(width):
        for y in range(height):
            tile = tiles[x][y]

            if not tile is None and not tile.image is None and tile.layer == layer:
                screen.blit(tile.image, ((x * blockSize) + offset[0], (y * blockSize) + offset[1]))

class TileType(enum.Enum):
    EMPTY = 0
    BRICK = 1
    CONCRETE = 2
    WATER = 3
    TREE = 4

class Tile:
    blocksMovement = True
    blocksProjectiles = False
    destroyable = False
    image = None
    hitpoints = 1
    layer = 0

    def __init__(self, tileType):
        self.setTileType(tileType)

    def setTileType(self, tileType):
        self.image = None
        self.tileType = tileType
        self.blocksMovement = False
        self.blocksProjectiles = False
        self.layer = 0

        if tileType == TileType.BRICK:
            self.image = images.get('brick')
            self.blocksMovement = True
            self.blocksProjectiles = True
        elif tileType == TileType.CONCRETE:
            self.image = images.get('concrete')
            self.blocksMovement = True
            self.blocksProjectiles = True
        elif tileType == TileType.WATER:
            self.image = images.get('water')
            self.blocksMovement = True
            self.blocksProjectiles = True
        elif tileType == TileType.TREE:
            self.image = images.get('tree')
            self.layer = 1

    def hitByProjectile(self, projectile, time):
        if self.tileType == TileType.BRICK:
            self.destroy()
        elif self.tileType == TileType.CONCRETE and projectile.getBreaksConcrete():
            self.destroy()

    def destroy(self):
        self.setTileType(TileType.EMPTY)