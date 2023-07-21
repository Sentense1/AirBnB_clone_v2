#!/usr/bin/python3
""" """

from flask import Flask
from models import storage
from models.state import State


app = Flask(__name__)

@app.teardown_appcontext
def teardown_app_contxt(exception):
    """ """
    storage.close()

@app.route('/states_list', strict_slashes=False)
def states_list():
    """ """
    states = sorted(storage.all(State).values(), key=lambda s: s.name)
    return render_template("7-states_list.html", states=states)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000)
