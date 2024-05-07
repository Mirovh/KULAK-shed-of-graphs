import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(graph, path, format):
    """Draws a graph and saves it to a file.

    Args:
        graph (nx.Graph): The graph to draw.
        path (str): The path to the file where the graph will be saved.
    """
    nx.draw(graph)
    plt.savefig(path, format=format)