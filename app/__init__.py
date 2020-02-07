#!/usr/bin/env python

from flask import Flask

from app.routes import routes
from app.assets import assets


app = Flask(__name__)
app.register_blueprint(routes)

# load static assets into application
assets.init_app(app)
