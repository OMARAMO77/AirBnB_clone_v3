#!/usr/bin/python3
"""---"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_cities(state_id):
    """Handle City objects"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([val.to_dict() for val in state.cities])
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        new_state = City(state_id=state_id, **post)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_city(city_id):
    """Handle a specific City object"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        city = storage.get('City', city_id)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)
                storage.save()
        return jsonify(city.to_dict()), 200
