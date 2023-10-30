#!/usr/bin/python3
"""---"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

classes = ("Amenity", "City", "Place", "Review", "State", "User")

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ returns a JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieve the number of each objects by type"""
    count_obj = {}
    for clas in classes:
        count_obj[clas] = storage.count(clas)

    return jsonify(count_obj)
