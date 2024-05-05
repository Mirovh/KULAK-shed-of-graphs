import unittest
import networkx as nx 
import plantriFilter as pf
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
        self.gh.saveHistory()
        self.gh.loadHistory()
        self.assertEqual(len(self.gh.history), 1)
        
    if __name__ == '__main__':
        unittest.main()
