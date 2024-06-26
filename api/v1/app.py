#!/usr/bin/python3
"""
This script shall start a Flask web application
"""
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from models import storage
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views, url_prefix="/api/v1")
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(teardown):
    """ This instance shall close the current session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ This instance shall return a JSON-formatted 404 response """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = getenv('HBNB_API_PORT', '5000')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True,
            debug=True)
