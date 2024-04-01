#!/usr/bin/python3
""" This script shall handle city objects and view them from REST API"""
from api.v1.views import app_views
from flask import jsonify, request, abort, Blueprint
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def ctts(state_id):
    """This instance shall return lst of all city obj (JSON)"""
    stt = storage.get("State", state_id)
    if stt is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([cty.to_dict() for cty in stt.cities])
    if request.method == 'POST':
        pst = request.get_json()
        if pst is None or type(pst) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        elif pst.get("name") is None:
            return jsonify({"error": "Missing name"}), 400
        pst["state_id"] = state_id
        neuvo_cty = City(**pst)
        neuvo_cty.save()
        return jsonify(neuvo_cty.to_dict()), 201


@app_views.route('/cities/<string:city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def gt_cty(city_id):
    """THis instance shall return the city objects by id also PUT & del"""
    cty = storage.get("City", city_id)
    if cty is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(cty.to_dict())
    if request.method == 'DELETE':
        cty.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        pst = request.get_json()
        if pst is None or type(pst) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        for cle, valu in pst.items():
            if cle not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(cty, cle, valu)
        cty.save()
        return jsonify(cty.to_dict()), 200
