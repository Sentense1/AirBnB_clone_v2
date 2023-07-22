#!/usr/bin/python3
"""Starts a Flask web application.
"""

from flask import Flask, request

app = Flask(__name__)


# Define the route for the root URL '/'
@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Displays 'Hello HBNB!'."""
    return "Hello HBNB!"


# Define the route for '/hbnb'
@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays 'HBNB'."""
    return "HBNB"


# Define the route for '/c/<text>'
@app.route('/c/<text>', strict_slashes=False)
def c_with_text(text):
    """Displays 'C' followed by the value of <text>."""
    # Replace underscores with spaces in the text variable
    formatted_text = text.replace('_', ' ')
    return "C {}".format(formatted_text)


if __name__ == "__main__":
    # Start the Flask development server
    # Listen on all available network interfaces (0.0.0.0) and port 5000
    app.run(host='0.0.0.0', port=5000)
