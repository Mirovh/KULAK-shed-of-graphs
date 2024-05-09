import time
from collections import deque
import os
import networkx as nx 
import json
from plantriFilter import Filter

class GraphHistory:
    def __init__(self, path='src/app/history/history.txt'):
        # Check for an environment variable to override the default path
        if 'SOG_HISTORY_PATH' in os.environ:
            path = os.environ['SOG_HISTORY_PATH'] + '/history.txt'
        self.pathName = path
        self.inputCount = 0
        self.outputCount = 0
        self.filterString = ''
        try:
            with open(self.pathName, 'r') as f:
                self.history = deque(f.readlines(), maxlen=20)
        except (FileNotFoundError, EOFError):
            self.history = deque(maxlen=20)

    def addGraph(self, graph, filterUsed):
        timestamp = time.time()
        self.inputCount += 1
        if isinstance(filterUsed, Filter):
            filterData = filterUsed.to_dict()
            self.filterString = json.dumps(filterData)
        else:
            self.filterString = filterUsed
        graphData = {
            'timestamp': timestamp,
            'inputCount': self.inputCount,
            'outputCount': self.outputCount,
            'filterString': self.filterString,
            'graph': list(graph.edges())
        }
        self.history.append(json.dumps(graphData))
        self.saveHistory()

    def saveHistory(self):
        print('Saving history')
        with open(self.pathName, 'w') as f:
            for graph in self.history:
                line = f"{time.time()}\t{len(self.history)}\t{len(self.history)}\t{self.filterString}\t{graph}\n"
                f.write(line)

    def loadHistory(self):
        with open(self.pathName, 'r') as f:
            self.history = deque(f.readlines(), maxlen=20)








