# pytest automatically injects fixtures
# that are defined in conftest.py
# in this case, client is injected
import json


def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["result"]["content"] == "hello world!"


def test_mirror(client):
    res = client.get("/mirror/Tim")
    assert res.status_code == 200
    assert res.json["result"]["name"] == "Tim"


def test_get_shows(client):
    res = client.get("/shows")
    assert res.status_code == 200

    shows = res.json["result"]["shows"]
    assert len(shows) == 3
    assert shows[0]["name"] == "Game of Thrones"


def test_get_shows_filtered(client):
    res = client.get("/shows?minEpisodes=3")
    assert res.status_code == 200

    shows = res.json["result"]["shows"]
    assert len(shows) == 2
    assert shows[0]["name"] == "Naruto"


def test_get_show_with_id(client):
    res = client.get("/shows/3")
    assert res.status_code == 200

    res_user = res.json["result"]
    assert res_user["name"] == "Black Mirror"
    assert res_user["episodes_seen"] == 3


def test_create_show(client):
    name = 'Breaking Bad'
    episodes_seen = 34
    res_success = client.post("/shows",
                              data=json.dumps({'name': name, 'episodes_seen': episodes_seen}),
                              content_type='application/json')
    assert res_success.status_code == 201

    res_user = res_success.json["result"]
    assert res_user["name"] == name
    assert res_user["episodes_seen"] == episodes_seen


def test_create_show_wrong_type(client):
    res_fail = client.post("/shows",
                           data=json.dumps(['a name']),  # wrong type
                           content_type='application/json')
    assert res_fail.status_code == 422


def test_create_show_missing_param(client):
    res_fail = client.post("/shows",
                           data=json.dumps({'name': 'a name'}),
                           content_type='application/json')
    assert res_fail.status_code == 422


def test_create_show_unexpected_param(client):
    res_fail = client.post("/shows",
                           data=json.dumps({'name': 'a name', 'episodes_seen': 1, 'description': ''}),
                           content_type='application/json')
    assert res_fail.status_code == 422


def test_update_show(client):
    new_episodes_seen = 4
    res = client.put("/shows/3",
                     data=json.dumps({'episodes_seen': new_episodes_seen}),
                     content_type='application/json')
    assert res.status_code == 201

    res_user = res.json["result"]
    assert res_user["name"] == 'Black Mirror'
    assert res_user["episodes_seen"] == new_episodes_seen
