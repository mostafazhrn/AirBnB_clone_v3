#!/usr/bin/python3
""" This script shall create new view for review that handles API actions """
from api.v1.views import app_views
from flask import jsonify, request, abort, Blueprint
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def re_views(place_id):
    """ This instance shall return a lst of Review objects in JSON"""
    plc = storage.get("Place", place_id)
    if plc is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([rev.to_dict() for rev in plc.reviews])
    if request.method == 'POST':
        pst = request.get_json()
        if pst is None or type(pst) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        elif pst.get("user_id") is None:
            return jsonify({"error": "Missing user_id"}), 400
        elif storage.get("User", pst.get("user_id")) is None:
            abort(404)
        elif pst.get("text") is None:
            return jsonify({"error": "Missing text"}), 400
        pst["place_id"] = place_id
        nuevo_rev = Review(**pst)
        nuevo_rev.save()
        return jsonify(nuevo_rev.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def gt_rev(review_id):
    """ This instance shall return a Review object in JSON after input ID"""
    rev = storage.get("Review", review_id)
    if rev is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(rev.to_dict())
    if requests.method == 'DELETE':
        rev.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        pst = request.get_json()
        if pst is None or type(pst) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        for cle, valu in pst.items():
            if cle not in ["id", "user_id", "place_id",
                           "created_at", "updated_at"]:
                setattr(rev, cle, valu)
        rev.save()
        return jsonify(rev.to_dict())
