import sys, os
import pytest
import networkx as nx
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
import GraphHistory
from plantriFilter import Filter

@pytest.fixture
def setup():
    gh = GraphHistory.GraphHistory('testPath')
    gh.saveHistory() # necessary because otherwise path may not exist
    gh.loadHistory()
    gh.history.clear()
    gh.saveHistory()
    filter1 = Filter('{"rules": [{"rule": "exact", "degree": 3, "count": 1}]}')
    filter2 = Filter('{"rules": [{"rule": "max", "degree": 4, "count": 1}]}')

    yield gh, filter1, filter2    # Run the test

    gh = None

def testAddGraph(setup):
    gh, filter1, _ = setup
    graph = nx.Graph()
    gh.addGraph(graph, filter1)
    assert len(gh.history) == 1
    assert json.loads(gh.history[0])['graph'] == list(graph.edges())
    assert json.loads(gh.history[0])['filterUsed'] == {'rules': [{"rule": "exact", 'degree': 3, 'count': 1}]}

def testSaveAndLoadHistory(setup):
    gh, filter1, _ = setup
    gh.loadHistory()
    graph = nx.Graph()
    gh.addGraph(graph, filter1)
    gh.saveHistory()
    gh.history.clear()
    gh.loadHistory()
    assert len(gh.history) == 1
    assert json.loads(gh.history[0].split('\t')[-1])['graph'] == list(graph.edges())
    assert json.loads(gh.history[0].split('\t')[-1])['filterUsed'] == {'rules': [{"rule": "exact", 'degree': 3, 'count': 1}]}

def testSaveAndLoadMultipleGraphs(setup):
    gh, filter1, filter2 = setup
    gh.loadHistory()
    graph1 = nx.Graph()
    graph2 = nx.Graph()
    gh.addGraph(graph1, filter1)
    gh.addGraph(graph2, filter2)
    gh.saveHistory()
    gh.history.clear()
    gh.loadHistory()
    assert len(gh.history) == 2
    assert json.loads(gh.history[0].split('\t')[-1])['graph'] == list(graph1.edges())
    assert json.loads(gh.history[1].split('\t')[-1])['graph'] == list(graph2.edges())
    assert json.loads(gh.history[0].split('\t')[-1])['filterUsed'] == {'rules': [{"rule": "exact", 'degree': 3, 'count': 1}]}
    assert json.loads(gh.history[1].split('\t')[-1])['filterUsed'] == {'rules': [{"rule": "max", 'degree': 4, 'count': 1}]}
    
def saveFilterRawJson(setup):
    gh, _, _ = setup
    graph = nx.Graph()
    gh.addGraph(graph, '{"rules": [{"rule": "exact", "degree": 3, "count": 1}]}')
    gh.saveHistory()
    gh.history.clear()
    gh.loadHistory()
    assert len(gh.history) == 1
    assert json.loads(gh.history[0].split('\t')[-1])['filterUsed'] == {'rules': [{"rule": "exact", 'degree': 3, 'count': 1}]}

def testFilename(setup):
    gh, _, _ = setup
    assert gh.pathName == 'testPath'

def testFileLocation(setup):
    assert os.path.exists('testPath')



