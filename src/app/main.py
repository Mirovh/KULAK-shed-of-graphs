import argparse
from drawGraph import draw_graph

def main():

    ########################################
    #   Argument parsing
    ########################################
    parser = argparse.ArgumentParser()
    parser.add_argument('image_folder', type=str, help='The folder where the images will be saved.')
    parser.add_argument('image_format', type=str, help='The format of the images to be saved.')
    args = parser.parse_args()


    ########################################
    #   Graph drawing
    ########################################
    allowed_formats = ['png', 'pdf', 'svg', 'eps', 'ps']
    if args.image_format != None and args.image_folder != None:
        if args.image_format not in allowed_formats:
            raise ValueError(f"Image format must be one of {allowed_formats}")
        def draw(graph):
            draw_graph(graph, args.image_folder, args.image_format)
    else:
        def draw(graph):
            pass


if __name__ == "__main__":
    main()