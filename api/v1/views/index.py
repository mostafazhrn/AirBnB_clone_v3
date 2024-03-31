#!/usr/bin/python3
"""
This script shall be the start of a Flask web application
"""
from api.v1.views import app_views
from flask import jsonify
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import json


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ This instance shall return a JSON-formatted status response """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ This instance shall return a JSON-formatted status response """
    obj = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    obj_dict = json.dumps(obj, indent=2)
    return obj_dict
