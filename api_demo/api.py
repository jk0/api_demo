#   Copyright 2015 Josh Kearney
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import argparse
import flask

from api_demo import version


APP = flask.Flask(__name__)

USERS = {}
GROUPS = {}


def _lookup_user(userid):
    """Lookup a user record."""
    return USERS[userid] if userid in USERS else None


def _lookup_group(group):
    """Lookup a group record."""
    return GROUPS[group] if group in GROUPS else None


def _set_groups(request, groups):
    """Create and assign groups to user records."""
    for group in groups:
        if not _lookup_group(group):
            # NOTE(jk0): If the group doesn't already exist, create it.
            GROUPS[group] = {"users": []}

        if request["userid"] not in GROUPS[group]["users"]:
            # NOTE(jk0): If the user is not already a member of the group, add
            # them.
            GROUPS[group]["users"].append(request["userid"])


@APP.route("/", methods=["GET"])
def index():
    """Handle index requests."""
    return version.version_string(), 200


@APP.route("/users/<userid>", methods=["GET"])
def get_user(userid):
    """Fetch and return a user record."""
    user = _lookup_user(userid)

    if not user:
        flask.abort(404)

    return flask.jsonify(user), 200


@APP.route("/users", methods=["POST"])
def create_user():
    """Create a new user record."""
    request = flask.request.get_json()

    try:
        # NOTE(jk0): We expect all of these keys to exist to be considered a
        # valid user record. Ignore all others.
        user = _lookup_user(request["userid"])

        if user:
            flask.abort(409)

        USERS[request["userid"]] = {
            "first_name": request["first_name"],
            "last_name": request["last_name"],
            "userid": request["userid"],
            "groups": request["groups"]
        }
    except KeyError:
        flask.abort(422)

    _set_groups(request, flask.request.json["groups"])

    return flask.jsonify(USERS[request["userid"]]), 201


@APP.route("/users/<userid>", methods=["DELETE"])
def delete_user(userid):
    """Delete a user record."""
    user = _lookup_user(userid)

    if not user:
        flask.abort(404)

    del USERS[userid]

    return "", 204


@APP.route("/users/<userid>", methods=["PUT"])
def update_user(userid):
    """Update a user record."""
    request = flask.request.get_json()
    user = _lookup_user(userid)

    if not user:
        flask.abort(404)

    try:
        # NOTE(jk0): We expect all of these keys to exist to be considered a
        # valid user record. Ignore all others.
        USERS[userid] = {
            "first_name": request["first_name"],
            "last_name": request["last_name"],
            # NOTE(jk0): This key is redundant, but per the spec, it has to
            # exist to be considered a valid user record.
            "userid": request["userid"],
            "groups": request["groups"]
        }
    except KeyError:
        flask.abort(422)

    _set_groups(request, flask.request.json["groups"])

    return flask.jsonify(USERS[userid]), 200


@APP.route("/groups/<group_name>", methods=["GET"])
def get_group(group_name):
    """Fetch and return a group record."""
    group = _lookup_group(group_name)

    if not group:
        flask.abort(404)

    return flask.jsonify(group), 200


@APP.route("/groups", methods=["POST"])
def create_group():
    """Create a new group record."""
    request = flask.request.get_json()

    try:
        group = _lookup_group(request["name"])
    except KeyError:
        flask.abort(422)

    if group:
        flask.abort(409)

    # NOTE(jk0): The spec says the body should only contain a `name` parameter,
    # but `flask.jsonify` purposely prevents us from doing that:
    #
    # http://bit.ly/1S1tDes
    GROUPS[request["name"]] = {"users": []}

    return flask.jsonify(GROUPS[request["name"]]), 201


@APP.route("/groups/<group_name>", methods=["PUT"])
def update_group(group_name):
    """Update a group record."""
    request = flask.request.get_json()
    group = _lookup_group(group_name)

    if not group:
        flask.abort(404)

    if type(request) is not list:
        # NOTE(jk0): The spec only accepts a list of IDs and not a dict of
        # lists.
        flask.abort(422)

    # NOTE(jk0): The spec says the body should be a list of IDs, but
    # `flask.jsonify` purposely prevents us from doing that:
    #
    # http://bit.ly/1S1tDes
    GROUPS[group_name] = {"users": request}

    return flask.jsonify(GROUPS[group_name]), 200


@APP.route("/groups/<group_name>", methods=["DELETE"])
def delete_group(group_name):
    """Delete a group record."""
    group = _lookup_group(group_name)

    if not group:
        flask.abort(404)

    del GROUPS[group_name]

    return "", 204


def main():
    """Run the API."""
    parser = argparse.ArgumentParser(version=version.version_string())
    parser.add_argument("--debug", action="store_true",
                        help="enable debug mode")
    parsed_args = parser.parse_args()

    APP.run(debug=parsed_args.debug)
