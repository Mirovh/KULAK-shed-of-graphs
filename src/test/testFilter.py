import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
import plantriFilter as pf
import networkx as nx
import json
import unittest

class TestPlantriFilter(unittest.TestCase):
    def setUp(self):
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

    def testFilterMaxMore(self):
        self.assertFalse(self.filterMax.sieve(self.graph4))
        self.assertFalse(self.filterMax.sieve(self.graph4Extra))

    def testFilterMaxLess(self):
        self.assertTrue(self.filterMax.sieve(self.graph2))
        self.assertTrue(self.filterMax.sieve(self.graph2Extra))

    def testFilterMaxEqual(self):
        self.assertTrue(self.filterMax.sieve(self.graph3))
        self.assertTrue(self.filterMax.sieve(self.graph3Extra))

    def testFilterMinMore(self):
        self.assertTrue(self.filterMin.sieve(self.graph4))
        self.assertTrue(self.filterMin.sieve(self.graph4Extra))

    def testFilterMinLess(self):
        self.assertFalse(self.filterMin.sieve(self.graph2))
        self.assertFalse(self.filterMin.sieve(self.graph2Extra))

    def testFilterMinEqual(self):
        self.assertTrue(self.filterMin.sieve(self.graph3))
        self.assertTrue(self.filterMin.sieve(self.graph3Extra))

    def testFilterOnlyTrue(self):
        self.assertTrue(self.filterOnly.sieve(self.graph2))
        self.assertTrue(self.filterOnly.sieve(self.graph3))
        self.assertTrue(self.filterOnly.sieve(self.graph4))

    def testFilterOnlyFalse(self):
        self.assertFalse(self.filterOnly.sieve(self.graph2Extra))
        self.assertFalse(self.filterOnly.sieve(self.graph3Extra))
        self.assertFalse(self.filterOnly.sieve(self.graph4Extra))

    def testFilterExactMore(self):
        self.assertFalse(self.filterExact.sieve(self.graph4))
        self.assertFalse(self.filterExact.sieve(self.graph4Extra))

    def testFilterExactLess(self):
        self.assertFalse(self.filterExact.sieve(self.graph2))
        self.assertFalse(self.filterExact.sieve(self.graph2Extra))

    def testFilterExactEqual(self):
        self.assertTrue(self.filterExact.sieve(self.graph3))
        self.assertTrue(self.filterExact.sieve(self.graph3Extra))

    def testFilterCombinationLess(self):
        self.assertFalse(self.filterCombination.sieve(self.graph2))
        self.assertFalse(self.filterCombination.sieve(self.graph2Extra))

    def testFilterCombinationLowerBound(self):
        self.assertTrue(self.filterCombination.sieve(self.graph3))
        self.assertTrue(self.filterCombination.sieve(self.graph3Extra))

    def testFilterCombinationUpperBound(self):
        self.assertTrue(self.filterCombination.sieve(self.graph4))
        self.assertTrue(self.filterCombination.sieve(self.graph4Extra))

    def testFilterCombinationMore(self):
        self.assertFalse(self.filterCombination.sieve(self.graph5))

class TestPlantriFilterParsing(unittest.TestCase):
    def setUp(self):
        with open("src/test/resources/RuleTarget.json", "r") as file:
            self.targetJson = json.load(file)
    
    def testParseStringCorrectFull(self):
        # Tests a string containing all the rules split by "and" with various capitalizations
        filter_string = "maximum 3 vertices with degree 2 and minimum 1 vertices with degree 3 and exactly 2 vertices with degree 4 and only vertices with degree 5"
        filter_json = pf.parse_string(filter_string)
        self.assertEqual(filter_json, self.targetJson)
        filter_string = "Maximum 3 vertices with degree 2 and Minimum 1 vertices with degree 3 and Exactly 2 vertices with degree 4 and Only vertices with degree 5"
        filter_json = pf.parse_string(filter_string)
        self.assertEqual(filter_json, self.targetJson)
        filter_string = "Maximum 3 vertices with degree 2 And Minimum 1 vertices with degree 3 And Exactly 2 vertices with degree 4 And Only vertices with degree 5"
        filter_json = pf.parse_string(filter_string)
        self.assertEqual(filter_json, self.targetJson)

    def testParseStringCorrectSingle(self):
        filter_string = "maximum 3 vertices with degree 2"
        filter_json = pf.parse_string(filter_string)
        self.assertEqual(filter_json, {"rules": [{"rule": "max", "degree": 2, "count": 3}]})

    def testParseStringFloat(self):
        filter_string = "maximum 3.5 vertices with degree 2"
        with self.assertRaises(pf.FilterStringError):
            pf.parse_string(filter_string)
        filter_string = "maximum 3,5 vertices with degree 2"
        with self.assertRaises(pf.FilterStringError):
            pf.parse_string(filter_string)

    def testParseStringIncorrect(self):
        filter_string = "nonsense 2 to 3 and 5"
        with self.assertRaises(pf.FilterStringError):
            pf.parse_string(filter_string)

    def testParseStringEmpty(self):
        filter_string = ""
        with self.assertRaises(pf.FilterStringError):
            pf.parse_string(filter_string)

    def testParseStringNoAnd(self):
        filter_string = "maximum 3 vertices with degree 2 minimum 1 vertices with degree 3 exactly 2 vertices with degree 4 only vertices with degree 5"
        with self.assertRaises(pf.FilterStringError):
            pf.parse_string(filter_string)

if __name__ == '__main__':
    unittest.main()