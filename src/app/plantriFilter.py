import sys
import networkx as nx
import re
import json

class Filter:
    rules = []

    #region Initialization
    
    def __init__(self, filter_string):
        try:
            # Try to parse the string as JSON
            self.filter = json.loads(filter_string)
        except json.JSONDecodeError:
            # If it's not valid JSON, treat it as a regular string
            self.filter = parse_string(filter_string)

        for rule in self.filter["rules"]:
            self.rules.append(rule)

    #endregion

    #region Filtering

    def sieve(self, graph):
        """Tests if the graph passes the filter rules.

        Args:
            graph (nx.Graph): The graph to test.
        """
        # Get the number of vertices for each degree
        degree_counts = {}
        for node in graph.nodes:
            degree = graph.degree(node)
            if degree not in degree_counts:
                degree_counts[degree] = 0
            degree_counts[degree] += 1
        # Check if the graph passes each rule
        for rule in self.rules:
            if not self._sieve_rule(rule, degree_counts):
                return False
        return True
    
    def _sieve_rule(self, rule, degree_counts):
        """Tests if the graph passes a single filter rule.

        Args:
            rule (dict): The rule to test.
            degree_counts (dict): The number of vertices for each degree.
        """
        try:
            if rule["rule"] == "min":
                degree = int(rule["degree"])
                min_count = int(rule["count"])
                return self._rule_min(degree, min_count, degree_counts)
            elif rule["rule"] == "max":
                degree = int(rule["degree"])
                max_count = int(rule["count"])
                return self._rule_max(degree, max_count, degree_counts)
            elif rule["rule"] == "exact":
                degree = int(rule["degree"])
                exact_count = int(rule["count"])
                return self._rule_exact(degree, exact_count, degree_counts)
            elif rule["rule"] == "only":
                degree = int(rule["degree"])
                return self._rule_only(degree, degree_counts)
            else:
                raise self.FilterJsonError("Unknown rule: " + rule["rule"])
        except:
            raise self.FilterJsonError("Could not parse rule: " + str(rule))
        
    def _rule_min(self, degree, count, degree_counts):
        """Tests if the graph has at least a certain number of vertices with a certain degree.

        Args:
            degree (int): The degree to test.
            count (int): The minimum number of vertices with that degree.
            degree_counts (dict): The number of vertices for each degree.
        """
        if degree not in degree_counts:
            return count <= 0
        return degree_counts[degree] >= count
    
    def _rule_max(self, degree, count, degree_counts):
        """Tests if the graph has at most a certain number of vertices with a certain degree.

        Args:
            degree (int): The degree to test.
            count (int): The maximum number of vertices with that degree.
            degree_counts (dict): The number of vertices for each degree.
        """
        if degree not in degree_counts:
            return count >= 0
        return degree_counts[degree] <= count
    
    def _rule_exact(self, degree, count, degree_counts):
        """Tests if the graph has exactly a certain number of vertices with a certain degree.

        Args:
            degree (int): The degree to test.
            count (int): The exact number of vertices with that degree.
            degree_counts (dict): The number of vertices for each degree.
        """
        if degree not in degree_counts:
            return count == 0
        return degree_counts[degree] == count
    
    def _rule_only(self, degree, degree_counts):
        """Tests if the graph has only vertices with a certain degree.

        Args:
            degree (int): The degree to test.
            degree_counts (dict): The number of vertices for each degree.
        """
        for other_degree in degree_counts:
            if other_degree != degree:
                return False
        return True

    class FilterJsonError(Exception):
        def __init__(self, message):
            self.message = message

    #endregion

def parse_string(filter_string):
    """Parses a filter string into a json object containing a list of rules.

    Args:
        filter_string (str): The filter string to parse.
    """
    # rules = []
    # for rule in filter_string.split(" and "):
    #     if re.match(r"minimum \d+ vertices with degree \d+", rule):
    #         min_match = re.match(r"minimum (\d+) vertices of degree (\d+)", rule)
    #         rules.append({"rule": "min", "degree": min_match.group(2), "count": min_match.group(1)})
    return None # TODO: Implement this

class FilterStringError(Exception):
        def __init__(self, message):
            self.message = message