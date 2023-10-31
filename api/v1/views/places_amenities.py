#!/usr/bin/python3
"""----"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
import models


@app_views.route('/places/<place_id>/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def manage_place_amenities(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        if models.storage_t == 'db':
            amenities = [amenity.to_dict() for amenity in place.amenities]
        else:
            amenities = [storage.get(Amenity, amenity_id).to_dict() for
                         amenity_id in place.amenity_ids]
        return jsonify(amenities)

    elif request.method == 'POST':
        amenity_id = request.json.get('amenity_id')
        if amenity_id is None:
            return jsonify({'error': 'Missing amenity_id'}), 400

        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            return jsonify({'error': 'amenity_id not found'}), 400

        if models.storage_t == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            place.amenities.append(amenity)
            storage.save()
        else:
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            place.amenity_ids.append(amenity_id)
            storage.save()

        return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if models.storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
        storage.save()

    return jsonify({}), 200
