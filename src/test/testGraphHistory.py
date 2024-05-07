import unittest
import networkx as nx 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
import GraphHistory as gh
import os

class TestGraphHistory(unittest.TestCase):
    def setUp(self):
        self.gh = gh.GraphHistory('testPath')
        self.gh.saveHistory() # necessary because otherwise path may not exist
        self.gh.loadHistory()
        self.gh.history.clear()
        self.gh.saveHistory()

    def testAddGraph(self):
        graph = nx.Graph()
        self.gh.addGraph(graph, 'filter')
        self.assertEqual(len(self.gh.history), 1)

    def testSaveAndLoadHistory(self):
        self.gh.loadHistory()
        graph = nx.Graph()
        self.gh.addGraph(graph, 'filter')
        self.gh.saveHistory()
        self.gh.history.clear()
        self.gh.loadHistory()
        self.assertEqual(len(self.gh.history), 1)

    def testSaveAndLoadMultipleGraphs(self):
        self.gh.loadHistory()
        graph1 = nx.Graph()
        graph2 = nx.Graph()
        self.gh.addGraph(graph1, 'filter1')
        self.gh.addGraph(graph2, 'filter2')
        self.gh.saveHistory()
        self.gh.history.clear()
        self.gh.loadHistory()
        self.assertEqual(len(self.gh.history), 2)

    def testFilename(self):
        self.assertEqual(self.gh.pathName, 'testPath')

    def testFileLocation(self):
        self.assertTrue(os.path.exists('testPath'))


        
if __name__ == '__main__':
    unittest.main()

