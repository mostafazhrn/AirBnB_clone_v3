#!/usr/bin/python3
""" This script shall create new view for User objects for RestFul API"""
from api.v1.views import app_views
from flask import jsonify, request, abort, Blueprint
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def usrs():
    """ This instance shall return a list of all User objects (JSON)"""
    if request.method == 'GET':
        return jsonify([usr.to_dict() for usr in storage.all("User")
                        .values()])
    if request.method == 'POST':
        pst = request.get_json()
        if pst is None or type(pst) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        elif pst.get("email") is None:
            return jsonify({"error": "Missing email"}), 400
        elif pst.get("password") is None:
            return jsonify({"error": "Missing password"}), 400
        nuevo_usr = User(**pst)
        nuevo_usr.save()
        return jsonify(nuevo_usr.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def gt_usr(user_id):
    """ This instance shall return User object in JSON format"""
    usr = storage.get("User", user_id)
    if usr is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(usr.to_dict())
    if request.method == 'DELETE':
        storage.delete(usr)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        pst = request.get_json()
        if pst is None or type(pst) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        for cle, valu in pst.items():
            if cle not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(usr, cle, valu)
        storage.save()
        return jsonify(usr.to_dict()), 200
