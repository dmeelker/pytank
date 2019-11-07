import playfield
from pathfinder import SearchGrid

class TankMover():
    def __init__(self, tank):
        self.tank = tank

class SearchGridGenerator():
    @staticmethod
    def generateSearchGridFromPlayfield():
        grid = SearchGrid(int(playfield.width / 2), int(playfield.height / 2))

        for x in range(grid.width):
            for y in range(grid.height):
                grid.set(x, y, SearchGridGenerator.getSearchSpaceCellValueForTileQuad(x, y))

        return grid

    @staticmethod
    def getSearchSpaceCellValueForTileQuad(searchSpaceX, searchSpaceY):
        tileSpaceX = searchSpaceX * 2
        tileSpaceY = searchSpaceY * 2
        
        return max( \
            SearchGridGenerator.getSearchSpaceCellValueFromPlayfield(tileSpaceX, tileSpaceY), \
            SearchGridGenerator.getSearchSpaceCellValueFromPlayfield(tileSpaceX + 1, tileSpaceY), \
            SearchGridGenerator.getSearchSpaceCellValueFromPlayfield(tileSpaceX, tileSpaceY + 1), \
            SearchGridGenerator.getSearchSpaceCellValueFromPlayfield(tileSpaceX + 1, tileSpaceY + 1))

    @staticmethod
    def getSearchSpaceCellValueFromPlayfield(x, y):
        tile = playfield.getTile(x, y)
        return SearchGridGenerator.getSearchSpaceCellValueForTile(tile)

    @staticmethod
    def getSearchSpaceCellValueForTile(tile):
        if tile is None:
            return 0
        elif tile.tileType == playfield.TileType.BRICK:
            return 1
        elif tile.tileType == playfield.TileType.CONCRETE:
            return 100
        elif tile.tileType == playfield.TileType.WATER:
            return 100
        else:
            return 0