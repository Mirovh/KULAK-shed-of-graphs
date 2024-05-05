import unittest
import networkx as nx 
import GraphHistory as gh

class TestGraphHistory(unittest.TestCase):
    def setUp(self):
        self.gh = gh.GraphHistory('testPath')

    def testAddGraph(self):
        graph = nx.Graph()
        self.gh.addGraph(graph, 'filter')
        self.assertEqual(len(self.gh.history), 1)

    def testSaveAndLoadHistory(self):
        graph = nx.Graph()
        self.gh.addGraph(graph, 'filter')
        self.gh.loadHistory()
        self.gh.history.clear()
        self.assertEqual(len(self.gh.history), 1)

    def testSaveAndLoadMultipleGraphs(self):
        graph1 = nx.Graph()
        graph2 = nx.Graph()
        self.gh.addGraph(graph1, 'filter1')
        self.gh.addGraph(graph2, 'filter2')
        self.gh.loadHistory()
        self.gh.history.clear()
        self.assertEqual(len(self.gh.history), 2)

        
    if __name__ == '__main__':
        unittest.main()

