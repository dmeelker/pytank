import playfield
from pathfinder import PathFinder
from pathfinder import SearchGrid

class PathProgress():
    def __init__(self, startLocation, targetLocation):
        self.startLocation = startLocation
        self.targetLocation = targetLocation
        self.plotPath(startLocation, targetLocation)

    def plotPath(self, startLocation, targetLocation):
        searchGrid = SearchGridGenerator.generateSearchGridFromPlayfield()
        pathFinder = PathFinder(searchGrid)

        self.path = pathFinder.find(startLocation, targetLocation)
        self.targetStepIndex = 1

    def moveToNextStepIfCurrentStepIsReached(self, currentLocation):
        if self.checkIfNextPathStepIsReached(currentLocation):
            if not self.targetReached():
                self.moveToNextTargetStep()
    
    def checkIfNextPathStepIsReached(self, currentLocation):
        targetLocation = self.path[self.targetStepIndex]
        targetLocation = (targetLocation[0] * 8, targetLocation[1] * 8)

        return currentLocation == targetLocation

    def moveToNextTargetStep(self):
        self.targetStepIndex += 1

    def targetReached(self):
        return self.targetStepIndex == len(self.path) - 1

    def getTarget(self):
        return self.targetLocation
    
    def getPath(self):
        return self.path

    def getTargetStepIndex(self):
        return self.targetStepIndex

    def getTargetStep(self):
        return self.path[self.targetStepIndex]

class SearchGridGenerator():
    @staticmethod
    def generateSearchGridFromPlayfield():
        grid = SearchGridGenerator.generateTerrainBasedGrid()
        SearchGridGenerator.accountForDoubleSize(grid) # fillGaps(grid)

        return grid

    @staticmethod
    def generateTerrainBasedGrid():
        grid = SearchGrid(playfield.width, playfield.height)

        for x in range(grid.width):
            for y in range(grid.height):
                grid.set(x, y, SearchGridGenerator.getSearchSpaceCellValueFromPlayfield(x, y))

        return grid

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
    def fillHorizontalGaps(grid):
        for y in range(grid.height):
            for x in range(grid.width):
                SearchGridGenerator.checkForHorizontalGap(grid, x, y)

    @staticmethod
    def checkForHorizontalGap(grid, x, y):
        if SearchGridGenerator.hasTwoHorizontalNeighbours(grid, x):
            values = [grid.get(x-1, y), grid.get(x, y), grid.get(x+1, y)]
            if values[0] > 0 and values[1] == 0 and values[2] > 0:
                grid.set(x, y, min(values[0], values[2]))

    @staticmethod
    def hasTwoHorizontalNeighbours(grid, x):
        return x > 0 and x < grid.width - 1

    @staticmethod
    def fillVerticalGaps(grid):
        for x in range(grid.width):
            for y in range(grid.height):
                SearchGridGenerator.checkForVerticalGap(grid, x, y)

    @staticmethod
    def checkForVerticalGap(grid, x, y):
        if SearchGridGenerator.hasTwoVerticalNeighbours(grid, y):
            values = [grid.get(x, y-1), grid.get(x, y), grid.get(x, y+1)]
            if values[0] > 0 and values[1] == 0 and values[2] > 0:
                grid.set(x, y, min(values[0], values[2]))

    @staticmethod
    def hasTwoVerticalNeighbours(grid, y):
        return y > 0 and y < grid.height - 1

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