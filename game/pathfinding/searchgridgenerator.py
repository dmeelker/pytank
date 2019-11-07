import playfield
from .searchgrid import SearchGrid

class SearchGridGenerator():
    @staticmethod
    def generateSearchGridFromPlayfield():
        grid = SearchGrid(playfield.width, playfield.height)
        SearchGridGenerator.generateTerrainBasedGrid(grid)
        SearchGridGenerator.accountForDoubleSize(grid)

        return grid

    @staticmethod
    def generateTerrainBasedGrid(grid):
        for x in range(grid.width):
            for y in range(grid.height):
                grid.set(x, y, SearchGridGenerator.getSearchSpaceCellValueFromPlayfield(x, y))

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
    def fillGaps(grid):
        SearchGridGenerator.fillHorizontalGaps(grid)
        SearchGridGenerator.fillVerticalGaps(grid)

    @staticmethod
    def getSearchSpaceCellValueFromPlayfield(x, y):
        tile = playfield.getTile(x, y)
        return SearchGridGenerator.getSearchSpaceCellValueForTile(tile)

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