#!/usr/bin/python3
"""Starts a Flask web application.
"""
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slahes = False


# Define the route for the root URL '/'
@app.route('/')
def hello_hbnb():
    """ Displays 'Hello HBNB! """
    return "Hello HBNB!"


if __name__ == "__main__":
    # Start the Flask development server
    # Listen on all available network interfaces (0.0.0.0) and port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
