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
    with open(self.pathName, 'a') as f:
        for i in range(0, len(self.history), 20):
            graphs = self.history[i:i+20]
            line = f"{time.time()}\t{len(self.history)}\t{len(self.history)}\t{self.filterString}\t{graphs}\n"
            f.write(line)

    def loadHistory(self):
        with open(self.pathName, 'rb') as f:
            self.history = pickle.load(f)
    
    if __name__ == "__main__":
        main()
