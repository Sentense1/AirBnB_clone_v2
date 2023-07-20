#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /: Displays 'Hello HBNB!'.
    /hbnb: Displays 'HBNB'.
    /c/<text>: Displays 'C' followed by the value of <text>.
    /python/(<text>): Displays 'Python' followed by the value of <text>.
    /number/<n>: Displays 'n is a number' only if <n> is an integer.
"""

from flask import Flask, request

app = Flask(__name__)

text = "is cool"

# Define the route for the root URL '/'
@app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"

# Define the route for '/hbnb'
@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"

# Define the route for '/c/<text>'
@app.route('/c/<text>', strict_slashes=False)
def c_with_text(text):
    # Replace underscores with spaces in the text variable
    formatted_text = text.replace('_', ' ')
    return "C {}".format(formatted_text)

# Define the route for '/python/(<text>)'
@app.route('/python/', defaults={'text': 'is_cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_with_text(text):
    # Replace underscores with spaces in the text variable
    formatted_text = text.replace('_', ' ')
    return "Python {}".format(formatted_text)

# Define the route for '/number/<n>'

if __name__ == "__main__":
    # Start the Flask development server
    # Listen on all available network interfaces (0.0.0.0) and port 5000
    app.run(host='0.0.0.0', port=5000)
