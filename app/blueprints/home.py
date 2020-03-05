from flask import Blueprint, render_template

# A Blueprint is just a way to split a Flask app
# into separate components to make it more organised
# Reference: http://exploreflask.com/en/latest/blueprints.html
home = Blueprint('routes', __name__,
                   template_folder='templates')


@home.route("/")
def root():
    return render_template("index.html")
