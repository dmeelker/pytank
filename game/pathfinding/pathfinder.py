import math
from utilities import PriorityQueue

class Node:
    def __init__(self, location, distance, estimatedDistance, parent, cellCost = 0):
        self.location = location
        self.distance = distance
        self.estimatedDistance = estimatedDistance
        self.cellCost = cellCost
        self.parent = parent
        self.recalculateCost()
    
    def recalculateCost(self):
        self.cost = self.distance + self.estimatedDistance + self.cellCost

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        return f'{self.location}, dist: {self.distance}, estdist: {self.estimatedDistance}, cost: {self.cost}'

class CoordinatesWithCost:
    def __init__(self, coordinates, cost):
        self.coordinates = coordinates
        self.cost = cost

class PathFinder:
    def __init__(self, searchSpace):
        self.searchSpace = searchSpace

    def find(self, startLocation, endLocation):
        self.initializeOpenAndClosedLists()        
        self.addStartLocationToOpenList(startLocation)

        while not self.openList.isEmpty():
            currentNode = self.getOpenNodeWithLowestCost()
            self.addToClosedList(currentNode.location)
            
            if currentNode.location == endLocation:
                return self.getPathFromEndNode(currentNode)

            self.considerAdjacentCells(currentNode, endLocation)

        return None

    def initializeOpenAndClosedLists(self):
        self.openList = PriorityQueue()
        self.closedList = set()

    def addStartLocationToOpenList(self, coordinates):
        self.openList.insert(Node(coordinates, 0, 0, None))

    def considerAdjacentCells(self, currentNode, endLocation):
        for adjacentCell in self.getAdjacentCells(currentNode):
            self.considerAdjacentCell(currentNode, adjacentCell, endLocation)

    def getAdjacentCells(self, node):
        coordinates = self.searchSpace.getAdjacentCellCoordinates(node.location[0], node.location[1])
        for adjacentCoordinates in coordinates:
            yield CoordinatesWithCost(adjacentCoordinates, self.searchSpace.get(adjacentCoordinates[0], adjacentCoordinates[1]))

    def canCellBeSkipped(self, cell):
        return self.inClosedList(cell.coordinates) or self.isCellImpenetrable(cell.cost)

    def inClosedList(self, coordinates):
        return coordinates in self.closedList

    def isCellImpenetrable(self, cellCost):
        return cellCost >= 100

    def considerAdjacentCell(self, currentNode, adjacentCell, endLocation):
        if self.canCellBeSkipped(adjacentCell):
            return
        else:
            existingNode = self.findOpenNodeByLocation(adjacentCell.coordinates)
            if existingNode != None:
                if self.isPathShorterViaOtherNode(currentNode, existingNode):
                    self.updatePathToNode(currentNode, existingNode)
            else:
                self.addAdjacentCellToOpenList(currentNode, adjacentCell, endLocation)
    
    def isPathShorterViaOtherNode(self, currentNode, nodeToCheck):
        return currentNode.cost + nodeToCheck.cellCost + 1 < nodeToCheck.cost

    def updatePathToNode(self, fromNode, toNode):
        toNode.parent = fromNode
        toNode.distance = fromNode.distance + 1
        toNode.recalculateCost()
        self.openList.heapify()

    def getOpenNodeWithLowestCost(self):
        return self.openList.getSmallest()
    
    def addAdjacentCellToOpenList(self, currentNode, adjacentCell, endLocation):
        estimatedDistance = self.estimateDistance(adjacentCell.coordinates, endLocation)
        newNode = Node(adjacentCell.coordinates, currentNode.distance + 1, estimatedDistance, currentNode, cellCost=adjacentCell.cost)
        self.addToOpenList(newNode)

    def addToOpenList(self, node):
        self.openList.insert(node)

    def addToClosedList(self, coordinates):
        self.closedList.add(coordinates)

    def estimateDistance(self, startLocation, endLocation):
        x = abs(endLocation[0] - startLocation[0])
        y = abs(endLocation[1] - startLocation[1])
        return x + y

    def findOpenNodeByLocation(self, location):
        for node in self.openList.getValues():
            if node.location == location:
                return node
        else:
            return None

    def getPathFromEndNode(self, node):
        steps = []
        currentNode = node

        while currentNode != None:
            steps.append(currentNode.location)
            currentNode = currentNode.parent
        steps.reverse()
        return steps