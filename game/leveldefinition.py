import tankspawnschedule
import playfield

class LevelDefinition():
    def __init__(self, size):
        self.size = size
        self.mapData = None
        self.tankSpawns = None
        self.baseLocation = None
        self.playerSpawnLocation = None

        self.initializeMapData()

    def initializeMapData(self):
        self.mapData = []

        for _ in range(self.size[0]):
            column = []
            for _ in range(self.size[1]):
                column.append(None)
            self.mapData.append(column)

    def getSize(self):
        return self.size

    def getMapData(self):
        return self.mapData

    def getTankSpawns(self):
        return self.tankSpawns

    def getBaseLocation(self):
        return self.baseLocation

    def getPlayerSpawnLocation(self):
        return self.playerSpawnLocation

class TankSpawnDefinition():
    def __init__(self, schedule):
        self.location = None
        self.schedule = schedule

    def getLocation(self):
        return self.location
    
    def getSchedule(self):
        return self.schedule

class LineReader():
    def __init__(self, lines):
        self.lines = lines
        self.index = -1

    def readLine(self):
        if self.index == len(self.lines):
            return None
        else: 
            self.index += 1
            return self.lines[self.index]

def loadFromString(levelString):
    reader = LineReader(levelString.splitlines())

    size = readLevelSize(reader)

    level = LevelDefinition(size)
    readSpawnSchedules(reader, level)
    readTileData(reader, level)

    return level

def readLevelSize(reader):
    line = reader.readLine()
    if not line.startswith('size='):
        raise Exception(f'Invalid size line {line}')

    values = line[5:].split(',')
    return (int(values[0]), int(values[1]))

def readSpawnSchedules(reader, level):
    spawnCount = readSpawnCount(reader)
    level.tankSpawns = []
    for _ in range(spawnCount):
        level.tankSpawns.append(TankSpawnDefinition(readSpawnSchedule(reader)))

def readSpawnCount(reader):
    line = reader.readLine()
    if not line.startswith('spawncount='):
        raise Exception(f'Invalid spawn count line {line}')

    return int(line[11:])

def readSpawnSchedule(reader):
    line = reader.readLine()
    return tankspawnschedule.TankSpawnSchedule.parseSpawnMomentsFromString(line)

foundTankSpawns = 0

def readTileData(reader, level):
    global foundTankSpawns
    foundTankSpawns = 0

    for y in range(level.getSize()[1]):
        line = reader.readLine()
        for x in range(level.getSize()[0]):
            character = line[x]
            interpretLevelLayoutCharacter(character, x, y, level)

def interpretLevelLayoutCharacter(character, x, y, level):
    global foundTankSpawns

    if character == 'B':
        level.getMapData()[x][y] = playfield.TileType.BRICK
    elif character == 'C':
        level.getMapData()[x][y] = playfield.TileType.CONCRETE
    elif character == '~':
        level.getMapData()[x][y] = playfield.TileType.WATER
    elif character == '^':
        level.getMapData()[x][y] = playfield.TileType.TREE
    elif character == 'X':
        level.baseLocation = (x, y)
    elif character == 'P':
        level.playerSpawnLocation = (x, y)
    elif character == 'S':
        level.tankSpawns[foundTankSpawns].location = (x,y)
        foundTankSpawns += 1