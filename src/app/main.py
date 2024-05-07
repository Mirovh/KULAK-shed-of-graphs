import argparse
from drawGraph import draw_graph
from plantriFilter import Filter
from GraphHistory import GraphHistory
import sys
import networkx as nx

def main():

    ########################################
    #   Argument parsing
    ########################################
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_folder', type=str, help='The folder where the images will be saved.')
    parser.add_argument('--image_format', type=str, help='The format of the images to be saved.')
    parser.add_argument('--filter_string', type=str, help='The filter string to apply to the graphs.')
    args = parser.parse_args()


    ########################################
    #   Graph drawing
    ########################################
    allowed_formats = ['png', 'pdf', 'svg', 'eps', 'ps']
    if args.image_format != None and args.image_folder != None:
        if args.image_format not in allowed_formats:
            raise ValueError(f"Image format must be one of {allowed_formats}")
        def draw(graph, id):
            draw_graph(graph, "src/app/" + str(args.image_folder) + "/graph" + str(id) + ".png", args.image_format)
    else:
        def draw(graph, id):
            pass

    ########################################
    #   Filter
    ########################################
    gh = GraphHistory()
    # If no filter string is provided, export the last passed graph from history
    if args.filter_string == None:
        # Export the last passed graph from history
        gh.loadHistory()
        graph = gh.history[-1]
        draw(graph, 0)
        return
    
    # Else, apply the filter string to the graphs and save the images if applicable
    # Make a filter object from the filter string
    filter = Filter(str(args.filter_string))

    # Continuously read the graph6 graphs from standard input
    for line in sys.stdin.buffer:
        line = line.strip()
        
        # Parse the graph6 graph into a NetworkX graph
        graph = nx.from_graph6_bytes(line)

        # Apply the filter rules to the graph
        filtered_graph = filter.sieve(graph)

        # If the graph passes the filter, print it in graph6 format, save to history and generate image if applicable
        if filtered_graph:
            print(graph)
            gh.addGraph(graph, filter)
            draw(graph, 0)
            print(f"Graph passed filter: {graph}")

if __name__ == "__main__":
    main()