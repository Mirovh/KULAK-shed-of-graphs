import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
import plantriFilter as pf
import networkx as nx
import json
import pytest


@pytest.fixture
def setup(self):
    with open("src/test/resources/RuleMax.json", "r") as file:
        self.filterMax = pf.Filter(file.read())
    with open("src/test/resources/RuleMin.json", "r") as file:
        self.filterMin = pf.Filter(file.read())
    with open("src/test/resources/RuleOnly.json", "r") as file:
        self.filterOnly = pf.Filter(file.read())
    with open("src/test/resources/RuleExact.json", "r") as file:
        self.filterExact = pf.Filter(file.read())
    with open("src/test/resources/RuleCombination.json", "r") as file:
        self.filterCombination = pf.Filter(file.read())
    self.graph2 = nx.MultiGraph()
    self.graph2.add_node(1)
    self.graph2.add_node(2)
    self.graph2.add_edge(1, 2)
    self.graph2.add_edge(2, 1)
    self.graph3 = nx.Graph()
    self.graph3.add_node(1)
    self.graph3.add_node(2)
    self.graph3.add_node(3)
    self.graph3.add_edge(1, 2)
    self.graph3.add_edge(2, 3)
    self.graph3.add_edge(3, 1)
    self.graph4 = nx.Graph()
    self.graph4.add_node(1)
    self.graph4.add_node(2)
    self.graph4.add_node(3)
    self.graph4.add_node(4)
    self.graph4.add_edge(1, 2)
    self.graph4.add_edge(2, 3)
    self.graph4.add_edge(3, 4)
    self.graph4.add_edge(4, 1)
    self.graph5 = nx.Graph()
    self.graph5.add_node(1)
    self.graph5.add_node(2)
    self.graph5.add_node(3)
    self.graph5.add_node(4)
    self.graph5.add_node(5)
    self.graph5.add_edge(1, 2)
    self.graph5.add_edge(2, 3)
    self.graph5.add_edge(3, 4)
    self.graph5.add_edge(4, 5)
    self.graph5.add_edge(5, 1)
    # We create additional graphs with an extra node with degree 0
    self.graph2Extra = self.graph2.copy()
    self.graph2Extra.add_node(3)
    self.graph3Extra = self.graph3.copy()
    self.graph3Extra.add_node(4)
    self.graph4Extra = self.graph4.copy()
    self.graph4Extra.add_node(5)

    yield   # Run the test

    self.graph2 = None
    self.graph3 = None
    self.graph4 = None
    self.graph5 = None
    self.graph2Extra = None
    self.graph3Extra = None
    self.graph4Extra = None
    self.filterMax = None
    self.filterMin = None
    self.filterOnly = None
    self.filterExact = None
    self.filterCombination = None


def test_filter_max_more(self):
    self.assertFalse(self.filterMax.sieve(self.graph4))
    self.assertFalse(self.filterMax.sieve(self.graph4Extra))

def test_filter_max_less(self):
    self.assertTrue(self.filterMax.sieve(self.graph2))
    self.assertTrue(self.filterMax.sieve(self.graph2Extra))

def test_filter_max_equal(self):
    self.assertTrue(self.filterMax.sieve(self.graph3))
    self.assertTrue(self.filterMax.sieve(self.graph3Extra))

def test_filter_min_more(self):
    self.assertTrue(self.filterMin.sieve(self.graph4))
    self.assertTrue(self.filterMin.sieve(self.graph4Extra))

def test_filter_min_less(self):
    self.assertFalse(self.filterMin.sieve(self.graph2))
    self.assertFalse(self.filterMin.sieve(self.graph2Extra))

def test_filter_min_equal(self):
    self.assertTrue(self.filterMin.sieve(self.graph3))
    self.assertTrue(self.filterMin.sieve(self.graph3Extra))

def test_filter_only_true(self):
    self.assertTrue(self.filterOnly.sieve(self.graph2))
    self.assertTrue(self.filterOnly.sieve(self.graph3))
    self.assertTrue(self.filterOnly.sieve(self.graph4))

def test_filter_only_false(self):
    self.assertFalse(self.filterOnly.sieve(self.graph2Extra))
    self.assertFalse(self.filterOnly.sieve(self.graph3Extra))
    self.assertFalse(self.filterOnly.sieve(self.graph4Extra))

def test_filter_exact_more(self):
    self.assertFalse(self.filterExact.sieve(self.graph4))
    self.assertFalse(self.filterExact.sieve(self.graph4Extra))

def test_filter_exact_less(self):
    self.assertFalse(self.filterExact.sieve(self.graph2))
    self.assertFalse(self.filterExact.sieve(self.graph2Extra))

def test_filter_exact_equal(self):
    self.assertTrue(self.filterExact.sieve(self.graph3))
    self.assertTrue(self.filterExact.sieve(self.graph3Extra))

def test_filter_combination_less(self):
    self.assertFalse(self.filterCombination.sieve(self.graph2))
    self.assertFalse(self.filterCombination.sieve(self.graph2Extra))

def test_filter_combination_lower_bound(self):
    self.assertTrue(self.filterCombination.sieve(self.graph3))
    self.assertTrue(self.filterCombination.sieve(self.graph3Extra))

def test_filter_combination_upper_bound(self):
    self.assertTrue(self.filterCombination.sieve(self.graph4))
    self.assertTrue(self.filterCombination.sieve(self.graph4Extra))

def test_filter_combination_more(self):
    self.assertFalse(self.filterCombination.sieve(self.graph5))

def test_filter_no_rules_json(self):
    with self.assertRaises(pf.FilterJsonError):
        pf.Filter("{}")

def test_filter_empty_rules_json(self):
    emptyFilter = pf.Filter("{\"rules\": []}")
    self.assertTrue(emptyFilter.sieve(self.graph2))
    self.assertTrue(emptyFilter.sieve(self.graph3))
    self.assertTrue(emptyFilter.sieve(self.graph4))
    self.assertTrue(emptyFilter.sieve(self.graph5))
    self.assertTrue(emptyFilter.sieve(self.graph2Extra))
    self.assertTrue(emptyFilter.sieve(self.graph3Extra))
    self.assertTrue(emptyFilter.sieve(self.graph4Extra))