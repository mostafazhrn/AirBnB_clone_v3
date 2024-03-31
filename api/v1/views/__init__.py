#!/usr/bin/python3
"""
This script shall create the blueprint for app_views
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


if (__name__ == "api.v1.views"):
    from api.v1.views.index import *
