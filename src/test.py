import app.plantriFilter as pf
import networkx as nx
import sys
import json

path = "C:\\Users\\Miro\\Documents\\0.Projects\\Informaticawerktuigen\\shed-of-graphs\\src\\ExampleRules.json"
with open(path, "r") as file:
    filter_json_string = file.read()
filter = pf.Filter(filter_json_string)
# make an example graph
graph = nx.Graph()
graph.add_node(1)
graph.add_node(2)
graph.add_node(3)
graph.add_node(4)
# Connect the nodes with every node except themselves
graph.add_edge(1, 2)
graph.add_edge(1, 3)
graph.add_edge(1, 4)
graph.add_edge(2, 3)
graph.add_edge(2, 4)
graph.add_edge(3, 4)
# print the degree of each node
print(graph.degree)

# apply the filter
print(filter.sieve(graph)) # This should return True

graph.add_node(5)

# apply the filter
print(filter.sieve(graph)) # This should return False