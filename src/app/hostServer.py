import flask
from GraphHistory import GraphHistory
from drawGraph import draw_graph

print('Starting server...', flush=True)

def main():
    gh = GraphHistory('~/backups/')

    # Create the Flask app
    app = flask.Flask(__name__)
    
    # Redirect root to index
    @app.route('/')
    def root():
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
    def serve_image(filename):
        # create an image with the id filename
        id = filename
        if len(gh.history) > int(id):
            graph = gh.history[id]
            draw_graph(graph, 'static/history/images/' + id + '.png')
            return flask.send_from_directory('static/history/images', id + '.png')
        else:
            return flask.send_from_directory('static/history/images', 'default.png')

    # Start the server
    app.run(debug=True)

if __name__ == '__main__':
    main()