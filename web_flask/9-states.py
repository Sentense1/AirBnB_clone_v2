#!/usr/bin/python3

from flask import Flask, render_template
from model import storage
from models.state import State
from models.city import city

app = Flask(__name__)

@app.teardown_appcontext
def teard0wn_app_context(exception):
    storage.close()

@app.route('/states', strict_slashes=False)
def states():
    """ """
    states = sorted(storage.all(State).values(), key=lambda s: s.name)
    return render_template("9-states.html", states=states)

@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id):
    state = storage.get(State, id)

    if state is None:
        return render_template("9-states.html")

    cities = sorted(state.cities, key=lambda c: c.name)
        if hasattr(state, 'cities') else state.cities()

    return render_template("9-states.html", state=state, citis=cities)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000)
