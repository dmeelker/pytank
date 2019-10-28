tiles = []
width = 0
height = 0

def initialize(w, h):
    global width, height
    width = w
    height = h
    initializeTiles()

def initializeTiles():
    global tiles
    tiles = []

    for x in range(width):
        column = []
        for y in range(height):
            column.append(None)
        
        tiles.append(column)

def setTile(x, y, tile):
    tiles[x][y] = tile

def getTile(x, y):
    return tiles[x][y]

def render(screen, offset):
    for x in range(width):
        for y in range(height):
            tile = tiles[x][y]

            if not tile is None:
                screen.blit(tile.image, ((x * 15) + offset[0], (y * 15) + offset[1]))

class Tile:
    blocksMovement = True
    image = None

    def __init__(self, image, blocksMovement = True):
        self.image = image
        self.blocksMovement = blocksMovement