try:
    import flask
except ImportError:
    while True:
        print("Failed import", flush=True)

while True:
    print("Hello, world!", flush=True)

# def main():
#     # Read the filter string from the command line argument
#     filter_string = sys.argv[1]

#     # Parse the filter string into filter rules
#     filter_rules = parse_filter_string(filter_string)

#     # Read the graph6 graph from standard input
#     graph6 = sys.stdin.readline().strip()

#     # Parse the graph6 graph into a NetworkX graph
#     graph = nx.parse_graph6(graph6)

#     # Apply the filter rules to the graph
#     filtered_graph = apply_filter(graph, filter_rules)

#     # Print the filtered graph in graph6 format
#     filtered_graph6 = nx.write_graph6(filtered_graph)
#     print(filtered_graph6)