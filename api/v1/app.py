#!/usr/bin/python3
"""runs flask server"""
from flask import Flask
from api.v1.views import app_views
from os import getenv
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """close session when finished"""
    storage.close()


@app.errorhandler(404)
def invalid_route(e):
    """handle 404 error"""
    return ({"error": "Not found"}, 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(threaded=True, host=host, port=port, debug=True)
