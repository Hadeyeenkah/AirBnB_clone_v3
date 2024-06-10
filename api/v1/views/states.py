#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage as s
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def define_state():
    """
    return the list of states
    """
    states = []
    states = s.all(State)
    for obj in states.values():
        states.append(obj.to_dict())
    return jsonify(states)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def creat_state():
    """
    create state route
    """
    state_request = request.get_json(silent=True)
    if state_request is None:
        abort(400, description='Not a JSON')
    if "name" not in state_request:
        abort(400, description='Missing name')
    new_state_object = State(**state_request)
    new_state_object.save()
    return jsonify(new_state_object.to_dict()), 201


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    gets a specific State object by ID
    :param state_id: state object id
    :return: state obj with the specified id or error
    """
    fetched = s.get(State, state_id)
    if not fetched:
        abort(404)
    return jsonify(fetched.to_dict())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    updates specific State object by ID
    """
    state_request = request.get_json(silent=True)
    if not request.get_json():
        abort(400, description='Not a JSON')
    fetched_obj = s.get(State, state_id)
    if not fetched_obj:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_dict()), 200


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete(state_id):
    """
    deletes State by id
    """
    fetched_obj = s.get(State, state_id)
    if not fetched_obj:
        abort(404)
    s.delete(fetched_obj)
    s.save()
    return jsonify({}), 200
