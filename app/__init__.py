#!/usr/bin/env python

from flask import Flask
from flask import g

from app.blueprints.home import home
from app.blueprints.api import api

from app.assets import assets


app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(api)

# load static assets into application
assets.init_app(app)
