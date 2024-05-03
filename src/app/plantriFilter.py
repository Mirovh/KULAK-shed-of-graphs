import sys
import networkx as nx
import re
import json

class Filter:
    """A filter for graph6 graphs based on the degree of vertices.
    
    Can be initialized with a filter string or a json object containing a list of rules.
    """

    #region Initialization
    
    def __init__(self, filter_string):
        try:
            # Try to parse the string as JSON
            self.filter = json.loads(filter_string)
        except json.JSONDecodeError:
            # If it's not valid JSON, treat it as a regular string
            self.filter = parse_string(filter_string)

        self.rules = []
        if "rules" not in self.filter:
            raise FilterJsonError("No rules found in json: " + str(self.filter))
        for rule in self.filter["rules"]:
            self.rules.append(rule)

    #endregion

    #region Filtering

    def sieve(self, graph) -> bool:
        """Tests if the graph passes the filter rules.

        Args:
            graph (nx.Graph): The graph to test.
        Returns:
            bool: True if the graph passes the filter rules, False otherwise.
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
        Returns:
            bool: True if the graph passes the rule, False otherwise.
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
                raise FilterJsonError("Unknown rule: " + rule["rule"])
        except:
            raise FilterJsonError("Could not parse rule: " + str(rule))
        
    def _rule_min(self, degree, count, degree_counts):
        """Tests if the graph has at least a certain number of vertices with a certain degree.

        Args:
            degree (int): The degree to test.
            count (int): The minimum number of vertices with that degree.
            degree_counts (dict): The number of vertices for each degree.
        Retuns:
            bool: True if the graph has at least the specified number of vertices with the specified degree, False otherwise.
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
        Returns:
            bool: True if the graph has at most the specified number of vertices with the specified degree, False otherwise.
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
        Returns:
            bool: True if the graph has exactly the specified number of vertices with the specified degree, False otherwise.
        """
        if degree not in degree_counts:
            return count == 0
        return degree_counts[degree] == count
    
    def _rule_only(self, degree, degree_counts):
        """Tests if the graph has only vertices with a certain degree.

        Args:
            degree (int): The degree to test.
            degree_counts (dict): The number of vertices for each degree.
        Returns:
            bool: True if the graph has only vertices with the specified degree, False otherwise.
        """
        for other_degree in degree_counts:
            if other_degree != degree:
                return False
        return True

    #endregion

def parse_string(filter_string):
    """Parses a filter string into a json object containing a list of rules.

    Args:
        filter_string (str): The filter string to parse.
    Returns:
        dict: A json object containing a list of rules.
    """
    rules = []
    for rule in filter_string.lower().split(" and "):
        if re.fullmatch(r"minimum \d+ vertices with degree \d+", rule):
            min_match = re.match(r"minimum (\d+) vertices with degree (\d+)", rule)
            rules.append({"rule": "min", "degree": int(min_match.group(2)), "count": int(min_match.group(1))})
        elif re.fullmatch(r"maximum \d+ vertices with degree \d+", rule):
            max_match = re.match(r"maximum (\d+) vertices with degree (\d+)", rule)
            rules.append({"rule": "max", "degree": int(max_match.group(2)), "count": int(max_match.group(1))})
        elif re.fullmatch(r"exactly \d+ vertices with degree \d+", rule):
            exa_match = re.match(r"exactly (\d+) vertices with degree (\d+)", rule)
            rules.append({"rule": "exact", "degree": int(exa_match.group(2)), "count": int(exa_match.group(1))})
        elif re.fullmatch(r"only vertices with degree \d+", rule):
            onl_match = re.match(r"only vertices with degree (\d+)", rule)
            rules.append({"rule": "only", "degree": int(onl_match.group(1))})
        else:
            raise FilterStringError("Could not parse rule \"" + rule + "\" in \"" + filter_string + "\"")
    return {"rules": rules}
    

class FilterStringError(Exception):
        def __init__(self, message):
            self.message = message

class FilterJsonError(Exception):
    def __init__(self, message):
        self.message = message

def main():
    # Read the filter string from the command line argument
    filter_string = sys.argv[1]

    # Make a filter object from the filter string
    filter = Filter(filter_string)

    # Continuously read the graph6 graphs from standard input
    for line in sys.stdin:
        graph6 = line.strip()

        # Parse the graph6 graph into a NetworkX graph
        graph = nx.parse_graph6(graph6)

        # Apply the filter rules to the graph
        filtered_graph = filter.sieve(graph)

        # If the graph passes the filter, print it in graph6 format
        if filtered_graph:
            filtered_graph6 = nx.write_graph6(graph)
            print(filtered_graph6)

if __name__ == "__main__":
    main()