#!/usr/bin/python3
"""Starts a Flask web application.
"""

from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


# Define the route for '/hbnb' and specify
#   strict_slashes=False to handle trailing slashes
@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Displays the main HBnB filters HTML page."""
    # Fetch all State, Amenity,
    #   and Place objects from the storage (FileStorage or DBStorage)
    states = storage.all("State")

    amenities = storage.all("Amenity")

    places = storage.all("Place")

    # Render the "100-hbnb.html" template and
    #   pass the fetched objects to the template
    return render_template("100-hbnb.html", states=states,
                           amenities=amenities, places=places)


# Teardown app context to remove the current
#   SQLAlchemy session after each request
@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    # Start the Flask development server
    # Listen on all available network interfaces (0.0.0.0) and port 5000
    app.run(host="0.0.0.0")
