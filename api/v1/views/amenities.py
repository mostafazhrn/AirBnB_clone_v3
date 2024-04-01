#!/usr/bin/python3
""" This script shall create new view for Amenity for RestFul API"""
from api.v1.views import app_views
from flask import jsonify, request, abort, Blueprint, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenit():
    """ This instance shall return a JSON_list of all Amenity objects """
    return jsonify([amn.to_dict() for amn in storage.all("Amenity").values()])


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def gt_amenit(amenity_id):
    """ This instance shall return a JSON-formatted Amenity object """
    amn = storage.get("Amenity", amenity_id)
    if amn is None:
        abort(404)
    return jsonify(amn.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenit(amenity_id):
    """ This instance shall delete a JSON-formatted Amenity object """
    amn = storage.get("Amenity", amenity_id)
    if amn is None:
        abort(404)
    amn.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def pst_amenit():
    """ This instance shall create a JSON-formatted Amenity object """
    pst = request.get_json()
    if not pst:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in pst:
        return jsonify({"error": "Missing name"}), 400
    new_amn = Amenity(**pst)
    storage.new(new_amn)
    storage.save()
    return make_response(jsonify(new_amn.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def gv_amenit(amenity_id):
    """ This instance shall update a JSON-formatted Amenity object """
    amn = storage.get("Amenity", amenity_id)
    if amn is None:
        abort(404)
    pst_bod = request.get_json()
    if not pst_bod:
        abort(400, "Not a JSON")
    for cle, valu in pst_bod.items():
        if cle != "id" and cle != "created_at" and cle != "updated_at":
            setattr(amn, cle, valu)
    storage.save()
    return make_response(jsonify(amn.to_dict()), 200)
