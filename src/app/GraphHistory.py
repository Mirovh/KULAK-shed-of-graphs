import pickle
import time
from collections import deque
import os

class GraphHistory:
    def __init__(self, path):
        self.pathName = path
        self.inputCount = 0
        self.outputCount = 0
        try:
            with open(self.pathName, 'rb') as f:
                self.history = pickle.load(f)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            self.history = deque(maxlen=20)

    def addGraph(self, graph, filterUsed):
        timestamp = time.time()
        self.inputCount += 1
        self.filterString = filterUsed
        graphData = {
            'timestamp': timestamp,
            'inputCount': self.inputCount,
            'outputCount': self.outputCount,
            'filterUsed': filterUsed,
            'graph': graph
        }
        self.history.append(graphData)
        self.saveHistory()

    def saveHistory(self):
        with open(self.pathName, 'wb') as f:
            pickle.dump(self.history, f)

    def loadHistory(self):
        with open(self.pathName, 'rb') as f:
            loaded_history = pickle.load(f)
        self.history.extend(loaded_history)

    def testFilename(self):
        self.assertEqual(self.gh.pathName, self.filename)

    def testFileLocation(self):
        self.assertTrue(os.path.exists(self.filename))




