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
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000)
