import sys, os
import pytest
import networkx as nx
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
import GraphHistory
@pytest.fixture
def setup():
    gh = GraphHistory.GraphHistory('testPath')
    gh.saveHistory() # necessary because otherwise path may not exist
    gh.loadHistory()
    gh.history.clear()
    gh.saveHistory()

    yield gh    # Run the test

    gh = None

def testAddGraph(setup):
    gh = setup
    graph = nx.Graph()
    gh.addGraph(graph, 'filter')
    assert len(gh.history) == 1
    assert eval(gh.history[0])['graph'] == list(graph.edges())

def testSaveAndLoadHistory(setup):
    gh = setup
    gh.loadHistory()
    graph = nx.Graph()
    gh.addGraph(graph, 'filter')
    gh.saveHistory()
    gh.history.clear()
    gh.loadHistory()
    assert len(gh.history) == 1
    assert eval(gh.history[0])['graph'] == list(graph.edges())

def testSaveAndLoadMultipleGraphs(setup):
    gh = setup
    gh.loadHistory()
    graph1 = nx.Graph()
    graph2 = nx.Graph()
    gh.addGraph(graph1, 'filter1')
    gh.addGraph(graph2, 'filter2')
    gh.saveHistory()
    gh.history.clear()
    gh.loadHistory()
    assert len(gh.history) == 2
    assert eval(gh.history[0])['graph'] == list(graph1.edges())
    assert eval(gh.history[1])['graph'] == list(graph2.edges())

def testFilename(setup):
    gh = setup
    assert gh.pathName == 'testPath'

def testFileLocation():
    assert os.path.exists('testPath')


