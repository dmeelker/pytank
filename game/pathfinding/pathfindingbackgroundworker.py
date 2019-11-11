import queue
import threading

from pathfinding.pathfinder import PathFinder

taskQueue = queue.Queue()
thread = None
running = False
stopRequested = False

def queueTask(task):
    taskQueue.put(task)

def reset():
    taskQueue = queue.Queue()

def start():
    global thread,stopRequested,running
    stopRequested = False

    thread = threading.Thread(target=workerFunction, daemon=True)
    thread.start()
    running = True

def stop():
    global stopRequested
    stopRequested = True
    thread.join()

def workerFunction():
    global running
    running = True

    while not stopRequested:
        try:
            task = taskQueue.get(block=True, timeout=0.01)
            processTask(task)
        except (queue.Empty):
            pass
        
    running = False

def processTask(task):
    path = PathFinder(task.searchGrid).find(task.startLocation, task.endLocation)
    task.setCompleted(path)

class Task():
    def __init__(self, searchGrid, startLocation, endLocation):
        self.searchGrid = searchGrid
        self.startLocation = startLocation
        self.endLocation = endLocation
        self.completed = False
        self.path = None
        self.lock = threading.Lock()
    
    def setCompleted(self, path):
        with self.lock:
            self.completed = True
            self.path = path
    
    def isCompleted(self):
        with self.lock:
            return self.completed

    def getPath(self):
        return self.path

    def pathFound(self):
        return self.path != None