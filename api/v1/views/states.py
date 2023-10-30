#!/usr/bin/python3
"""---"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def handle_states():
    """Handle State objects"""
    if request.method == 'GET':
        states = storage.all(State).values()
        return jsonify([state.to_dict() for state in states])
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in data:
            return jsonify({'error': 'Missing name'}), 400
        state = State(**data)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_state(state_id):
    """Handle a specific State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in data.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(state, key, value)
                storage.save()
        return jsonify(state.to_dict()), 200
