#!/usr/bin/python3
"""Starts a Flask web application.
"""
from flask import Flask, request

app = Flask(__name__)
app.url_map.strict_slashes = False


# Define the route for the root URL '/'
@app.route('/')
def hello_hbnb():
    """Displays 'Hello HBNB!'."""
    return "Hello HBNB!"


# Define the route for '/hbnb'
@app.route('/hbnb')
def hbnb():
    """Displays 'HBNB'."""
    return "HBNB"


# Define the route for '/c/<text>'
@app.route('/c/<text>')
def c_with_text(text):
    """Displays 'C' followed by the value of <text>.

    Replaces any underscores in <text> with slashes.
    """
    # Replace underscores with spaces in the text variable
    formatted_text = text.replace('_', ' ')
    return "C {}".format(formatted_text)


# Define the route for '/python/(<text>)'
@app.route('/python/', defaults={'text': 'is_cool'})
@app.route('/python/<text>')
def python_with_text(text):
    """Displays 'Python' followed by the value of <text>.

    Replaces any underscores in <text> with slashes.
    """
    # Replace underscores with spaces in the text variable
    formatted_text = text.replace('_', ' ')
    return "python{}".format(formatted_text)


# Define the route for '/number/<n>'
@app.route('/number/<int:n>')
def number(n):
    """Displays 'n is a number' only if n is an integer."""
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
