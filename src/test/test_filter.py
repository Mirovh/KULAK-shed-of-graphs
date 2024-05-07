import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
import plantriFilter as pf
import networkx as nx
import json
import pytest


@pytest.fixture
def setup():
    with open("src/test/resources/RuleMax.json", "r") as file:
        filterMax = pf.Filter(file.read())
    with open("src/test/resources/RuleMin.json", "r") as file:
        filterMin = pf.Filter(file.read())
    with open("src/test/resources/RuleOnly.json", "r") as file:
        filterOnly = pf.Filter(file.read())
    with open("src/test/resources/RuleExact.json", "r") as file:
        filterExact = pf.Filter(file.read())
    with open("src/test/resources/RuleCombination.json", "r") as file:
        filterCombination = pf.Filter(file.read())
    graph2 = nx.MultiGraph()
    graph2.add_node(1)
    graph2.add_node(2)
    graph2.add_edge(1, 2)
    graph2.add_edge(2, 1)
    graph3 = nx.Graph()
    graph3.add_node(1)
    graph3.add_node(2)
    graph3.add_node(3)
    graph3.add_edge(1, 2)
    graph3.add_edge(2, 3)
    graph3.add_edge(3, 1)
    graph4 = nx.Graph()
    graph4.add_node(1)
    graph4.add_node(2)
    graph4.add_node(3)
    graph4.add_node(4)
    graph4.add_edge(1, 2)
    graph4.add_edge(2, 3)
    graph4.add_edge(3, 4)
    graph4.add_edge(4, 1)
    graph5 = nx.Graph()
    graph5.add_node(1)
    graph5.add_node(2)
    graph5.add_node(3)
    graph5.add_node(4)
    graph5.add_node(5)
    graph5.add_edge(1, 2)
    graph5.add_edge(2, 3)
    graph5.add_edge(3, 4)
    graph5.add_edge(4, 5)
    graph5.add_edge(5, 1)
    # We create additional graphs with an extra node with degree 0
    graph2Extra = graph2.copy()
    graph2Extra.add_node(3)
    graph3Extra = graph3.copy()
    graph3Extra.add_node(4)
    graph4Extra = graph4.copy()
    graph4Extra.add_node(5)

    yield graph2, graph3, graph4, graph5, graph2Extra, graph3Extra, graph4Extra, filterMax, filterMin, filterOnly, filterExact, filterCombination   # Run the test

    graph2 = None
    graph3 = None
    graph4 = None
    graph5 = None
    graph2Extra = None
    graph3Extra = None
    graph4Extra = None
    filterMax = None
    filterMin = None
    filterOnly = None
    filterExact = None
    filterCombination = None


def test_filter_max_more(setup):
    _, _, graph4, _, _, _, graph4Extra, filterMax, _, _, _, _ = setup
    assert not filterMax.sieve(graph4)
    assert not filterMax.sieve(graph4Extra)

def test_filter_max_less(setup):
    graph2, _, _, _, graph2Extra, _, _, filterMax, _, _, _, _ = setup
    assert filterMax.sieve(graph2)
    assert filterMax.sieve(graph2Extra)

def test_filter_max_equal(setup):
    _, graph3, _, _, _, graph3Extra, _, filterMax, _, _, _, _ = setup
    assert filterMax.sieve(graph3)
    assert filterMax.sieve(graph3Extra)

def test_filter_min_more(setup):
    _, _, graph4, _, _, _, graph4Extra, _, filterMin, _, _, _ = setup
    assert filterMin.sieve(graph4)
    assert filterMin.sieve(graph4Extra)

def test_filter_min_less(setup):
    graph2, _, _, _, graph2Extra, _, _, _, filterMin, _, _, _ = setup
    assert not filterMin.sieve(graph2)
    assert not filterMin.sieve(graph2Extra)

def test_filter_min_equal(setup):
    _, graph3, _, _, _, graph3Extra, _, _, filterMin, _, _, _ = setup
    assert filterMin.sieve(graph3)
    assert filterMin.sieve(graph3Extra)

def test_filter_only_true(setup):
    graph2, graph3, graph4, _, _, _, _, _, _, filterOnly, _, _ = setup
    assert filterOnly.sieve(graph2)
    assert filterOnly.sieve(graph3)
    assert filterOnly.sieve(graph4)

def test_filter_only_false(setup):
    _, _, _, _, graph2Extra, graph3Extra, graph4Extra, _, _, filterOnly, _, _ = setup
    assert not filterOnly.sieve(graph2Extra)
    assert not filterOnly.sieve(graph3Extra)
    assert not filterOnly.sieve(graph4Extra)

def test_filter_exact_more(setup):
    _, _, graph4, _, _, _, graph4Extra, _, _, _, filterExact, _ = setup
    assert not filterExact.sieve(graph4)
    assert not filterExact.sieve(graph4Extra)

def test_filter_exact_less(setup):
    graph2, _, _, _, graph2Extra, _, _, _, _, _, filterExact, _ = setup
    assert not filterExact.sieve(graph2)
    assert not filterExact.sieve(graph2Extra)

def test_filter_exact_equal(setup):
    _, graph3, _, _, _, graph3Extra, _, _, _, _, filterExact, _ = setup
    assert filterExact.sieve(graph3)
    assert filterExact.sieve(graph3Extra)

def test_filter_combination_less(setup):
    graph2, _, _, _, graph2Extra, _, _, _, _, _, _, filterCombination = setup
    assert not filterCombination.sieve(graph2)
    assert not filterCombination.sieve(graph2Extra)

def test_filter_combination_lower_bound(setup):
    _, graph3, _, _, _, graph3Extra, _, _, _, _, _, filterCombination = setup
    assert filterCombination.sieve(graph3)
    assert filterCombination.sieve(graph3Extra)

def test_filter_combination_upper_bound(setup):
    _, _, graph4, _, _, _, graph4Extra, _, _, _, _, filterCombination = setup
    assert filterCombination.sieve(graph4)
    assert filterCombination.sieve(graph4Extra)

def test_filter_combination_more(setup):
    _, _, _, graph5, _, _, _, _, _, _, _, filterCombination = setup
    assert not filterCombination.sieve(graph5)

def test_filter_no_rules_json():
    with pytest.raises(pf.FilterJsonError):
        pf.Filter("{}")

def test_filter_empty_rules_json(setup):
    graph2, graph3, graph4, graph5, graph2Extra, graph3Extra, graph4Extra, _, _, _, _, _ = setup
    emptyFilter = pf.Filter("{\"rules\": []}")
    assert emptyFilter.sieve(graph2)
    assert emptyFilter.sieve(graph3)
    assert emptyFilter.sieve(graph4)
    assert emptyFilter.sieve(graph5)
    assert emptyFilter.sieve(graph2Extra)
    assert emptyFilter.sieve(graph3Extra)
    assert emptyFilter.sieve(graph4Extra)