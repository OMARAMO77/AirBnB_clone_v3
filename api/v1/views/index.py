#!/usr/bin/python3
"""---"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ returns a JSON"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieve the number of each objects by type"""
    objects = {"amenities": 'Amenity', "cities": 'City', "places": 'Place',
               "reviews": 'Review', "states": 'State', "users": 'User'}
    for key, value in objects.items():
        objects[key] = storage.count(value)
    return jsonify(objects)
