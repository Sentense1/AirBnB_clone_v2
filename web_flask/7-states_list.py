#!/usr/bin/python3

from flask import Flask, render_template, teardown_appcontext
from models import storage, State
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_storage(error):
    """Closes the storage after each request."""
    storage.close()


@app.route('/states_list')
def states_list():
    """Displays a list of all State objects present in DBStorage."""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda s: s.name)

    return render_template('7-states_list.html', states=sorted_states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
