import pickle
import time
from collections import deque

class GraphHistory:
    def __init__(self, path):
        self.pathName = path
        self.inputCount = 0
        self.outputCount = 0
        try:
            with open(self.pathName, 'rb') as f:
                self.history = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self.history = deque(maxlen=20)

    def add_graph(self, graph, filterUsed):
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
        self.save_history()

    def save_history(self, pathName):
        with open(pathName, 'a') as f:
            for i in range(0, len(self.history['recent graphs']), 20):
                graphs = self.history['recent graphs'][i:i+20]
                line = f"{time.time()}\t{len(self.history['input graphs'])}\t{len(self.history['output graphs'])}\t{self.filterString}\t{graphs}\n"
                f.write(line)

    def load_history(self):
        with open(self.pathName, 'rb') as f:
            self.history = pickle.load(f)
