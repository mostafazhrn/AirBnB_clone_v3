#!/usr/bin/python3
""" This script shall start a Flask web application """
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from models import storage
from models.state import State
from os import getenv


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ This instance shall return a JSON-formatted status response """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def gt_stats():
    """ This instance shall return a stat resp in JSON form """
    ob = {"amenities": "Amenity", "cities": "City", "places": "Place",
          "reviews": "Review", "states": "State", "users": "User"}
    for cle, valu in ob.items():
        ob[cle] = storage.count(valu)
    return jsonify(ob)
