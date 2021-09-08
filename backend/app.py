import dataclasses
from typing import Tuple, Type, TypeVar

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


@app.route("/shows", methods=['GET'])
def get_all_shows():
    shows: list = db.get('shows')

    min_episodes = request.args.get('minEpisodes')
    if min_episodes is not None:
        shows = [s for s in shows if s['episodes_seen'] >= int(min_episodes)]

    return create_response({"shows": shows})


@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    db.deleteById('shows', int(id))
    return create_response(message="Show deleted")


# TODO: Implement the rest of the API here!

@app.route("/shows/<id>", methods=['GET'])
def get_show(id):
    show = db.getById('shows', int(id))
    if show is None:
        return create_response(status=404, message="No show with this id exists")
    return create_response(show)


@dataclasses.dataclass
class ShowPayload:
    name: str
    episodes_seen: int


TDataclass = TypeVar('TDataclass')


def init_dataclass(data: dict, klass: Type[TDataclass]) -> TDataclass:
    """
    Constructs a dataclass by validating that `data` provides the necessary
    arguments to all (non-InitVar and non-ClassVar) fields

    :param data: the data with which to initialize the dataclass
    :param klass: the type of dataclass to initialize
    :return: an initialized instance of the dataclass
    """
    valid_fields = {}
    for field in dataclasses.fields(klass):
        field_name = field.name
        field_value = data.pop(field_name, None)
        if field_value is None:
            raise ValueError(f'Missing attribute: {field_name!r}')
        valid_fields[field_name] = field_value

    # This is a debatable design decision since this goes against the Robustness principle (we raise an exception on
    # unexpected attributes, while we could just as well ignore them and accept the data). However, I prefer a
    # "fail-fast" approach, especially when we control the front-end (this can help in discovering bugs)
    if len(data) > 0:
        attr = data.popitem()[0]  # get any unexpected attribute
        raise ValueError(f'Unexpected attribute: {attr!r}')

    return klass(**valid_fields)


@app.route("/shows", methods=['POST'])
def create_show():
    request_json = request.get_json()
    if not isinstance(request_json, dict):
        return create_response(status=422, message=f"JSON body must be of type 'object': {type(request_json)!r}")

    try:
        show: ShowPayload = init_dataclass(request_json, ShowPayload)
    except ValueError as e:
        return create_response(status=422, message=str(e))

    new_show = db.create('shows', dataclasses.asdict(show))
    return create_response(new_show, status=201)


@app.route("/shows/<id>", methods=['PUT'])
def update_show(id):
    request_json = request.get_json()
    if not isinstance(request_json, dict):
        return create_response(status=422, message=f"JSON body must be of type 'object': {type(request_json)!r}")

    show = db.updateById('shows', int(id), request_json)
    if show is None:
        return create_response(status=404, message="No show with this id exists")

    return create_response(show, status=201)


"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
