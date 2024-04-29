import networkx as nx
import sys
import json

def filter_graph(graph, rules):
    # Get the degrees of all vertices in the graph
    degrees = [d for n, d in graph.degree()]
    
    # Check each rule
    for rule, value in rules.items():
        # Parse the rule name and value
        rule_parts = rule.split('_')
        rule_type = rule_parts[0]
        rule_degree = int(rule_parts[1])
        
        # Count the number of vertices with the given degree
        count = degrees.count(rule_degree)
        
        # Check the rule
        if rule_type == 'min' and count < value:
            return False
        elif rule_type == 'max' and count > value:
            return False
        elif rule_type == 'exact' and count != value:
            return False
    
    # If all rules pass, the graph passes the filter
    return True

def main():
    # Read the graph6 graph from standard input
    graph6 = sys.stdin.read().strip()
    # Convert the graph6 string to a networkx graph
    graph = nx.from_graph6_bytes(graph6.encode('utf-8'))
    
    # Read the filter rules from the command line argument
    rules = json.loads(sys.argv[1])
    
    # Filter the graph
    if filter_graph(graph, rules):
        # If the graph passes the filter, print it to standard output
        print(graph6)

if __name__ == "__main__":
    main()