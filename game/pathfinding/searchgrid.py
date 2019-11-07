class SearchGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.initialize()

    def initialize(self):
        self.data = [0 for i in range(self.width * self.height)]
    
    def get(self, x, y):
        return self.data[(y*self.width) + x]

    def set(self, x, y, value):
        self.data[(y*self.width) + x] = value

    def containsCoordinates(self, x, y):
        return not (x < 0 or x >= self.width or y < 0 or y >= self.height)

    def getAdjacentCellCoordinates(self, x, y):
        adjacentCoordinates = []

        if x > 0:
            adjacentCoordinates.append((x-1, y))
        if x < self.width - 1:
            adjacentCoordinates.append((x+1, y))
        if y > 0:
            adjacentCoordinates.append((x, y-1))
        if y < self.height - 1:
            adjacentCoordinates.append((x, y+1))

        return adjacentCoordinates