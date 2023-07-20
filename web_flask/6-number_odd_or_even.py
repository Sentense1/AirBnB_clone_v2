#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /: Displays 'Hello HBNB!'.
    /hbnb: Displays 'HBNB'.
    /c/<text>: Displays 'C' followed by the value of <text>.
    /python/(<text>): Displays 'Python' followed by the value of <text>.
    /number/<n>: Displays 'n is a number' only if <n> is an integer.
    /number_template/<n>: Displays an HTML page only if <n> is an integer.
        - Displays the value of <n> in the body.
    /number_odd_or_even/<n>: Displays an HTML page only if <n> is an integer.
        - States whether <n> is even or odd in the body.
"""

from flask import Flask, request, render_template

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
@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_with_text(text):
    # Replace underscores with spaces in the text variable
    formatted_text = text.replace('_', ' ')
    return "Python {}".format(formatted_text)

# Define the route for '/number/<n>'
@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    return "{} is a number".format(n)

# Define the route for '/number_template/<n>'
@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    # Check if n is an integer
    if isinstance(n, int):
        # Render the template and pass the value of n to the template
        return render_template('number_template.html', n=n)
    else:
        # If n is not an integer, return an error message
        return "Invalid input. Please provide an integer."

# Define the route for '/number_odd_or_even/<n>'

if __name__ == "__main__":
    # Start the Flask development server
    # Listen on all available network interfaces (0.0.0.0) and port 5000
    app.run(host='0.0.0.0', port=5000)
