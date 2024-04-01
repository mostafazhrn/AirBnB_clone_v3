#!/usr/bin/python3
""" This script shall create new view for Place that handles RestFul API"""
from api.v1.views import app_views
from flask import jsonify
from flask import request, abort
from flask import Blueprint
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def plcs(city_id):
    """ This instance shall return lst of Places objs in a format JSON """
    ctt = storage.get("City", city_id)
    if ctt is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([plc.to_dict() for plc in ctt.places])
    if request.method == 'POST':
        pst = request.get_json()
        if pst is None or type(pst) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        elif pst.get("user_id") is None:
            return jsonify({"error": "Missing user_id"}), 400
        elif storage.get("User", pst.get("user_id")) is None:
            abort(404)
        elif pst.get("name") is None:
            return jsonify({"error": "Missing name"}), 400
        nuevo_plc = place(**pst)
        nuevo_plc.city_id = city_id
        nuevo_plc.save()
        return jsonify(nuevo_plc.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def gt_place(place_id):
    """ This instance shall return a Place object based on id (JSON)"""
    plc = storage.get("Place", place_id)
    if plc is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(plc.to_dict())
    if request.method == 'DELETE':
        plc.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        pst = request.get_json()
        if pst is None:
            return jsonify({"error": "Not a JSON"}), 400
        for cle, valu in pst.items():
            if cle not in ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']:
                setattr(plc, cle, valu)
        plc.save()
        return jsonify(plc.to_dict()), 200
