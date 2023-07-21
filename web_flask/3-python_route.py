#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /: Displays 'Hello HBNB!'
"""

from flask import Flask, request

app = Flask(__name__)

@app.route('/', strict_slashes=False)

def hello_hbnb():
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"

@app.route('/c/<text>', strict_slashes=False)
def c_with_text(text):
    formatted_text = text.replace('_', ' ')
    return "C {}".format(formatted_text)

@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_with_text(text):
    # Replace underscores with spaces in the text variable
    formatted_text = text.replace('_', ' ')
    return "Python {}".format(formatted_text)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port =5000)
