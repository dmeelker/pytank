tiles = []
width = 0
height = 0
pixelWidth = 0
pixelHeight = 0
blockSize = 8

def initialize(w, h):
    global width, height, pixelWidth, pixelHeight
    width = w
    height = h
    pixelWidth = w * blockSize
    pixelHeight = h * blockSize
    initializeTiles()

def initializeTiles():
    global tiles
    tiles = []

    for _ in range(width):
        column = []
        for _ in range(height):
            column.append(None)
        
        tiles.append(column)

def setTile(x, y, tile):
    tiles[x][y] = tile

def getTile(x, y):
    return tiles[x][y]

def getTileAtPixel(x, y):
    tileX = int(x / blockSize)
    tileY = int(y / blockSize)

    if not containsTileCoordinates(tileX, tileY):
        return None

    return tiles[tileX][tileY]

def convertPixelToTileCoordinates(pixelCoordinates):
    return (int(pixelCoordinates[0] / blockSize), int(pixelCoordinates[1] / blockSize))

def containsTileCoordinates(x, y):
    return not (x < 0 or x >= width or y < 0 or y >= height)

def containsPixelCoordinates(x, y):
    return not (x < 0 or x >= pixelWidth or y < 0 or y >= pixelHeight)

def render(screen, offset, layer):
    for x in range(width):
        for y in range(height):
            tile = tiles[x][y]

            if not tile is None and not tile.image is None and tile.layer == layer:
                screen.blit(tile.image, ((x * blockSize) + offset[0], (y * blockSize) + offset[1]))

class Tile:
    blocksMovement = True
    blocksProjectiles = False
    destroyable = False
    image = None
    hitpoints = 1
    layer = 0

    def __init__(self, image, blocksMovement = True, destroyable = False, blocksProjectiles = False, hitpoints = 1, layer = 0):
        self.image = image
        self.blocksMovement = blocksMovement
        self.destroyable = destroyable
        self.blocksProjectiles = blocksProjectiles
        self.hitpoints = hitpoints
        self.layer = layer

    def hitByProjectile(self, projectile):
        if self.destroyable:
            self.hitpoints -= projectile.power
            if self.hitpoints <= 0:
                self.blocksMovement = False
                self.blocksProjectiles = False
                self.image = None
