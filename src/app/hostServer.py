import flask
from GraphHistory import GraphHistory
from drawGraph import draw_graph
import subprocess
import os
import networkx as nx
from plantriFilter import Filter

print('Starting server...', flush=True)

def main():
    gh = GraphHistory()

    # Create the Flask app
    app = flask.Flask(__name__)
    
    # Redirect root to index
    @app.route('/')
    def root():
        print('redirecting to index', flush=True)
        return flask.redirect(flask.url_for('index'))

    # Serve index.html using Flask at index endpoint
    @app.route('/index')
    def index():
        response = flask.make_response(flask.send_from_directory('static', 'index.html'))
        response.headers["Accept-CH"] = "Sec-CH-Prefers-Color-Scheme"
        response.headers["Vary"] = "Sec-CH-Prefers-Color-Scheme"
        response.headers["Critical-CH"] = "Sec-CH-Prefers-Color-Scheme"
        return response
    
    # Serve main.js using Flask at mainScript endpoint
    @app.route('/mainScript')
    def mainScript():
        return flask.send_from_directory('static', 'main.js')
    
    # Define routes to serve different favicon images
    @app.route('/static/icons/<path:filename>')
    def serve_favicon(filename):
        # Check if the user's browser prefers dark mode
        prefers_dark_mode = flask.request.headers.get('Sec-CH-Prefers-Color-Scheme') == 'dark'
        
        # Determine the appropriate favicon filename based on the user's preference
        if prefers_dark_mode:
            # Serve the white favicon for dark mode
            return flask.send_from_directory('static/icon_dark_mode', filename)
        else:
            # Serve the default favicon for light mode
            return flask.send_from_directory('static/icon_light_mode', filename)
        
    @app.route('/history/images/<path:filename>')
    def serve_graph_image(filename):
        # create an image with the id filename
        id = filename
        if len(gh.history) > int(id):
            graph = gh.history[int(id)]['graph']
            # Check for a path to override the default path
            if 'SOG_IMG_PATH' in os.environ:
                path = os.environ['SOG_IMG_PATH']
                path2 = path
            else:
                path = 'src/app/history/images'
                path2 = 'history/images'
            draw_graph(graph, path + '/graph' + id + '.png', 'png')
            return flask.send_from_directory(path2, 'graph' + id + '.png')
        else:
            # return a 404 error
            return flask.abort(404)
        
    @app.route('/history/<path:filename>', methods=['POST'])
    def serve_graph(filename):
        # get the request data
        data = flask.request.get_json()
        # get the value for fullinfostring
        fullinfostring = data['fullinfostring']
        # If the fullinfostring is true, return the full history
        # get the graph with the id filename
        gh.loadHistory()
        id = filename
        if len(gh.history) > int(id):
            graph = gh.history[int(id)]['graph']
            if isinstance(graph, nx.Graph) and fullinfostring == 'true':
                # Convert the graph to a string representation
                graph = nx.to_dict_of_dicts(graph)
            # send graph as json
            return flask.jsonify({"graphString": str(graph), "success": True})
        else:
            # return a 404 error
            return flask.abort(404)
        
    # define a POST route to submit a graph filter task
    @app.route('/filter', methods=['POST'])
    def submit_filter_request():
        # get the request data
        data = flask.request.get_json()
        # get the graph order from the request data
        order = data['order']
        # get the filter from the request data
        filter = data['filter']
        minDegree = data['minDegree']
        
        # Before running, check the following things
        # 1. Check if the filter is valid
        try:
            Filter(str(filter))
        except Exception as e:
            print(e, flush=True)
            return flask.jsonify({"success": False, "error": str(e)})
        # 2. Check if the order is valid (must be a positive integer < 14)
        try:
            order = int(order)
            assert order >= 1
            assert order < 14
        except Exception as e:
            print("ordererror: " + str(order), flush=True)
            return flask.jsonify({"success": False, "error": "Invalid order. Must be a positive integer < 14."})
        # 3. Check if the minDegree is valid (must be a positive integer or None)
        try:
            if minDegree != None:
                minDegree = int(minDegree)
                assert minDegree >= 0
        except Exception as e:
            print("mindegreeerror: " + str(minDegree), flush=True)
            return flask.jsonify({"success": False, "error": "Invalid minDegree. Must be a positive integer or None."})
        
        # Run the plantri command and pipe the output to the main.py script
        if minDegree == None:
            minDegree = 3
        minDegreeParsed = "-c1m" + str(minDegree)
        # Check if running in container
        if os.environ.get('DOCKER_CONTAINER') is not None:
            process1 = subprocess.Popen(['plantri', '-g', '-p', minDegreeParsed, str(order)], stdout=subprocess.PIPE)
            process2 = subprocess.Popen(['python3', 'main.py', '--image_format', 'png', '--image_folder', os.environ.get('SOG_IMG_PATH'), '--filter_string', str(filter)], stdin=process1.stdout, stdout=subprocess.PIPE)
        else:
            process1 = subprocess.Popen(['plantri', '-g', '-p', minDegreeParsed, str(order)], stdout=subprocess.PIPE)
            process2 = subprocess.Popen(['python3', 'src/app/main.py', '--image_format', 'png', '--image_folder', 'history/images', '--filter_string', str(filter)], stdin=process1.stdout, stdout=subprocess.PIPE)
        for line in iter(process2.stdout.readline, b''):
            print(line.decode(), end='')
        return flask.jsonify({"success": True})

    # Start the server
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()