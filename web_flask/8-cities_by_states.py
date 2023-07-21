#!/usr/bin/python3
""" """

from flask import Flask
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)

@app.teardown_appcontext
def teardown_app_contxt(exception):
    """ """
    storage.close()

@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    states = sorted(storage.all(State).values(), key=lambda s: s.name)
    return render_template("8-cities_by_states.html", states=states)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000)
