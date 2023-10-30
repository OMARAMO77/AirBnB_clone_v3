#!/usr/bin/python3
"""----"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' not in data:
            return jsonify({'error': 'Missing user_id'}), 400
        if 'text' not in data:
            return jsonify({'error': 'Missing text'}), 400
        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)
        data['place_id'] = place_id
        review = Review(**data)
        storage.new(review)
        storage.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in data.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
