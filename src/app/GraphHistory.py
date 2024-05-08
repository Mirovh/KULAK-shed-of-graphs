import time
from collections import deque

class GraphHistory:
    def __init__(self, path):
        self.pathName = path
        self.inputCount = 0
        self.outputCount = 0
        try:
            with open(self.pathName, 'r') as f:
                self.history = deque(f.readlines(), maxlen=20)
        except (FileNotFoundError, EOFError):
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
        self.history.append(str(graphData))
        self.saveHistory()

    def saveHistory(self):
        with open(self.pathName, 'a') as f:
            for graph in self.history:
                line = f"{time.time()}\t{len(self.history)}\t{len(self.history)}\t{self.filterString}\t{graph}\n"
                f.write(line)


    def loadHistory(self):
        with open(self.pathName, 'r') as f:
            self.history = deque(f.readlines(), maxlen=20)






