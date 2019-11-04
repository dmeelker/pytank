import heapq

class Node:
    def __init__(self, location, distance, estimatedDistance, parent):
        self.location = location
        self.distance = distance
        self.estimatedDistance = estimatedDistance
        self.cost = distance + estimatedDistance
        self.parent = parent
    
    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        return f'{self.location}, dist: {self.distance}, estdist: {self.estimatedDistance}, cost: {self.cost}'

class PriorityQueue:
    def __init__(self):
        self.values = []

    def insert(self, value):
        print(f'Inserting {value}')
        heapq.heappush(self.values, value)

    def heapify(self):
        heapq.heapify(self.values)

    def getSmallest(self):
        return heapq.heappop(self.values)

    def isEmpty(self):
        return len(self.values) == 0

class SearchGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.initialize()

    def initialize(self):
        self.data = []

        for x in range(self.width):
            row = []
            for y in range(self.height):
               row.append(0)
            self.data.append(row)
    
    def get(self, x, y):
        return self.data[x][y]

    def set(self, x, y, value):
        self.data[x][y] = value

    def containsCoordinates(self, x, y):
        return not (x < 0 or x >= self.width or y < 0 or y >= self.height)

    def getAdjacentCellCoordinates(self, x, y):
        adjacentCells = []

        if x > 0:
            adjacentCells.append((x-1, y))
        if x < self.width - 1:
            adjacentCells.append((x+1, y))
        if y > 0:
            adjacentCells.append((x, y-1))
        if y < self.height - 1:
            adjacentCells.append((x, y+1))

        return adjacentCells


class PathFinder:
    def __init__(self, searchSpace):
        self.searchSpace = searchSpace
        self.openList = PriorityQueue()
        self.closedList = set()

    def estimateDistance(self, startLocation, endLocation):
        x = abs(endLocation[0] - startLocation[0])
        y = abs(endLocation[1] - startLocation[1])
        return (x*x) + (y*y)

    def find(self, startLocation, endLocation):
        self.addToOpenList(Node(startLocation, 0, 0, None))
        
        currentNode = None
        path = None

        while not self.openList.isEmpty():
            currentNode = self.openList.getSmallest()
            self.closedList.add(currentNode.location)
            
            if currentNode.location == endLocation:
                return self.backTrackNode(currentNode)

            for adjacentCell in self.searchSpace.getAdjacentCellCoordinates(currentNode.location[0], currentNode.location[1]):
                cellValue = self.searchSpace.get(adjacentCell[0], adjacentCell[1])
                if adjacentCell in self.closedList or cellValue == -1:
                    continue
                
                existingNode = self.findOpenNodeByLocation(adjacentCell)
                if existingNode != None:
                    if currentNode.cost + 1 < existingNode.cost:
                        existingNode.parent = currentNode
                        existingNode.distance = currentNode.distance + 1
                        existingNode.cost = existingNode.distance + existingNode.estimatedDistance + cellValue
                        self.openList.heapify()
                else:
                    estimatedDistance = self.estimateDistance(adjacentCell, endLocation)
                    newNode = Node(adjacentCell, currentNode.distance + 1, estimatedDistance, currentNode)
                    self.addToOpenList(Node(adjacentCell, currentNode.distance + 1, estimatedDistance, currentNode))
                
        return None

    def backTrackNode(self, node):
        steps = []
        currentNode = node

        while currentNode != None:
            steps.append(currentNode.location)
            currentNode = currentNode.parent
        steps.reverse()
        return steps

    def addToOpenList(self, node):
        self.openList.insert(node)

    def findOpenNodeByLocation(self, location):
        for node in self.openList.values: # Nope!
            if node.location == location:
                return node
        else:
            return None