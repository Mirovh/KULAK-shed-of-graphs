import flask

print('Starting server...', flush=True)

def main():
    app = flask.Flask(__name__)
    
    # Redirect root to index
    @app.route('/')
    def root():
        return flask.redirect(flask.url_for('index'))

    # Serve index.html using Flask at index endpoint
    @app.route('/index')
    def index():
        return flask.send_from_directory('static', 'index.html')

    # Start the server
    app.run()

if __name__ == '__main__':
    main()