import playfield
from pathfinding.searchgrid import SearchGrid

class SearchGridGenerator():
    @staticmethod
    def generateSearchGridFromPlayfield(cellValueFunction = None):
        cellValueFunction = cellValueFunction or SearchGridGenerator.getSearchSpaceCellValueForTile
        grid = SearchGrid(playfield.width, playfield.height)
        SearchGridGenerator.generateTerrainBasedGrid(grid, cellValueFunction)
        SearchGridGenerator.accountForDoubleSize(grid)

        return grid

    @staticmethod
    def generateTerrainBasedGrid(grid, cellValueFunction):
        for x in range(grid.width):
            for y in range(grid.height):
                tile = playfield.getTile(x, y)
                grid.set(x, y, cellValueFunction(tile))

    @staticmethod
    def accountForDoubleSize(grid):
        for y in range(grid.height):
            for x in range(grid.width):
                if x < grid.width - 1:
                    values = [grid.get(x, y), grid.get(x + 1, y)]
                    if values[1] > 0 and values[0] == 0:
                        grid.set(x, y, values[1])

                if y < grid.height - 1:
                    values = [grid.get(x, y), grid.get(x, y + 1)]
                    if values[1] > 0 and values[0] == 0:
                        grid.set(x, y, values[1])

    @staticmethod
    def getSearchSpaceCellValueForTile(tile):
        if tile is None:
            return 0
        elif tile.tileType == playfield.TileType.BRICK:
            return 8
        elif tile.tileType == playfield.TileType.CONCRETE:
            return 100
        elif tile.tileType == playfield.TileType.WATER:
            return 100
        else:
            return 0