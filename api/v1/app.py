#!/usr/bin/python3
"""Main Flask module"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(self):
    storage.close()


@app.errorhandler(404)
def invalid_route(e):
    """handle 404 error"""
    return ({"error": "Not found"}, 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(threaded=True, host=host, port=port, debug=True)
