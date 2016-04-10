"""
Just a basic flask app - the real work is in downloading the elastic search
info and downloading it into the database, which happens in the entry point of
the Docker container.
"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    """index method returns success automatically."""
    return 'Success'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
