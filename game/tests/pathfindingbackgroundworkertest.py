import unittest
import time

import pathfinding.pathfindingbackgroundworker as worker
from pathfinding.pathfindingbackgroundworker import Task
from pathfinding.searchgrid import SearchGrid
from pathfinding.plannedpath import PlannedPath

class PathfindingBackgroundWorkerTest(unittest.TestCase):
    def setUp(self):
        worker.reset()

    def test_queueTask(self):
        task = Task(None, None, None)

        worker.queueTask(task)
        self.assertEqual(task, worker.taskQueue.get())

    def test_startStop(self):
        worker.start()
        self.assertTrue(worker.running)
        worker.stop()
        self.assertFalse(worker.running)

    def test_processTask(self):
        task = Task(SearchGrid(2, 2), (0,0), (1,0))

        worker.start()
        worker.queueTask(task)
        time.sleep(0.05)
        worker.stop()

        self.assertTrue(task.isCompleted())
        self.assertEqual([(0,0), (1,0)], task.getPath())
