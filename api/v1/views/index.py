#!/usr/bin/python3
"""
This script shall be the start of a Flask web application """
from api.v1.views import app_views
from flask import jsonify
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from models.state import State
from os import getenv


@app.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ This instance shall return a JSON-formatted status response """
    return jsonify({"status": "OK"})
