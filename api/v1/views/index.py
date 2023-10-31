#!/usr/bin/python3
"""---"""
from api.v1.views import app_views
from models import storage
from flask import jsonify

classes = ("Amenity", "City", "Place", "Review", "State", "User")


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ returns a JSON"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieve the number of each objects by type"""
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(cls)
    return jsonify(count_dict)
