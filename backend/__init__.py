#!/usr/bin/env python

from flask import Flask
from flask_cors import CORS

from backend.blueprints.api import api

app = Flask(__name__)
app.register_blueprint(api)

CORS(app)
