import math
import heapq

def radiansToDegrees(radians):
    return radians * (180/math.pi)

def degreesToRadians(degrees):
    return degrees * (math.pi / 180)

def vectorFromDegrees(degrees):
    radians = degreesToRadians(degrees)
    return Vector(math.cos(radians), math.sin(radians))

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return str(self.x) + "," + str(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def add(self, otherVector):
        return Vector(self.x + otherVector.x, self.y + otherVector.y)
    
    def subtract(self, otherVector):
        return Vector(self.x - otherVector.x, self.y - otherVector.y)
    
    def multiplyScalar(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
        
    def round(self):
        return Vector(round(self.x), round(self.y))

    def toUnit(self):
        length = self.length()
        return Vector(self.x / length, self.y / length)

    def toTuple(self):
        return (self.x, self.y)

    def toIntTuple(self):
        return (int(self.x), int(self.y))
    
    def length(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y))
    
    def angleInDegrees(self):
        return radiansToDegrees(math.atan2(self.y, self.x))
        
    def limitLength(self, maxLength):
        length = self.length()
        return self.toUnit().multiplyScalar(min(length, maxLength))

    @staticmethod
    def fromTuple(tuple):
        return Vector(tuple[0], tuple[1])

vectorLeft = Vector(-1, 0)
vectorRight = Vector(1, 0)
vectorUp = Vector(0, -1)
vectorDown = Vector(0, 1)

class PriorityQueue:
    def __init__(self):
        self.values = []

    def insert(self, value):
        heapq.heappush(self.values, value)

    def heapify(self):
        heapq.heapify(self.values)

    def getSmallest(self):
        return heapq.heappop(self.values)

    def isEmpty(self):
        return len(self.values) == 0

    def getValues(self):
        return self.values

class Timer:
    def __init__(self, interval):
        self.interval = interval
        self.lastIntervalTime = 0

    def update(self, time):
        if time - self.lastIntervalTime > self.interval:
            self.lastIntervalTime = time
            return True
        else:
            return False
    
    def setInterval(self, interval):
        self.interval = interval