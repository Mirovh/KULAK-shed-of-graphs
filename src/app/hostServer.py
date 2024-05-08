import flask
from GraphHistory import GraphHistory
from drawGraph import draw_graph
import subprocess
import os

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
        print(flask.request.headers)
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
        
    @app.route('/history/<path:filename>')
    def serve_graph(filename):
        # get the graph with the id filename
        gh.loadHistory()
        id = filename
        if len(gh.history) > int(id):
            graph = gh.history[int(id)]['graph']
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
        # Run the plantri command and pipe the output to the main.py script
        # Check if running in container
        if os.environ.get('DOCKER_CONTAINER') is not None:
            process1 = subprocess.Popen(['plantri', '-g', '-p', str(order)], stdout=subprocess.PIPE)
            process2 = subprocess.Popen(['python3', 'main.py', '--image_format', 'png', '--image_folder', os.environ.get('SOG_IMG_PATH'), '--filter_string', str(filter)], stdin=process1.stdout, stdout=subprocess.PIPE)
        else:
            process1 = subprocess.Popen(['plantri', '-g', '-p', str(order)], stdout=subprocess.PIPE)
            process2 = subprocess.Popen(['python3', 'src/app/main.py', '--image_format', 'png', '--image_folder', 'history/images', '--filter_string', str(filter)], stdin=process1.stdout, stdout=subprocess.PIPE)
        for line in iter(process2.stdout.readline, b''):
            print(line.decode(), end='')
        print(f"Handled filter request with order {order} and filter {filter}")
        print('done')
        return flask.jsonify({"success": True})

    # Start the server
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()