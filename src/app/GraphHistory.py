import time
from collections import deque
import os
import networkx as nx 
from networkx.readwrite import json_graph
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
            self.loadHistory()
        except (FileNotFoundError, EOFError):
            self.history = deque(maxlen=20)

    def addGraph(self, graph, filterUsed):
        timestamp = time.time()
        self.inputCount += 1
        if isinstance(filterUsed, Filter):
            rules = filterUsed.rules
            filterData = {
                'rules': rules
            }
            self.filterString = json.dumps(filterData)
        elif isinstance(filterUsed, str) and 'rules' in json.loads(filterUsed):
            self.filterString = filterUsed
        else:
            self.filterString = json.dumps({'filterUsed': 'default value'})
        graphData = {
            'timestamp': timestamp,
            'inputCount': self.inputCount,
            'outputCount': self.outputCount,
            'filterUsed': self.filterString,
            'graph': graph
        }
        self.history.append(graphData)
        self.saveHistory()

    def saveHistory(self):
        with open(self.pathName, 'w') as f:
            for graphData in self.history:
                line = f"{graphData['timestamp']}\t{graphData['inputCount']}\t{graphData['outputCount']}\t{json.dumps(graphData['filterUsed'])}\t" + "{ \"nxGraph\": " + json.dumps(json_graph.adjacency_data(graphData['graph'])) + " }\n"
                f.write(line)

    def loadHistory(self):
        with open(self.pathName, 'r') as f:
            self.history = deque(maxlen=20)
            for line in f.readlines():
                parts = line.strip().split('\t')
                graphData = {
                    'timestamp': float(parts[0]),
                    'inputCount': int(parts[1]),
                    'outputCount': int(parts[2]),
                    'filterUsed': json.loads(parts[3]),
                    'graph': json_graph.adjacency_graph(json.loads(parts[4])["nxGraph"])  
                }
                self.history.append(graphData)











