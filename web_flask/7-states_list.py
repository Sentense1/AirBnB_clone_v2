#!/usr/bin/python3
""" Starts a Flask web application. """
from flask import Flask, render_template
from models import storage


# creates an instance of the Flask class and assigns
# it to the variable app
app = Flask(__name__)


# Teardown app context to remove the
#   current SQLAlchemy session after each request
@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session."""
    storage.close()


# Define the route for '/states_list'
@app.route('/states_list', strict_slashes=False)
def states_list():
    """ displays a HTML page with a list of states """
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
