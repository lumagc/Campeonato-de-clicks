import pytest
from app import create_app
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


# Test para obtener todos las localidades
def test_getLocalities(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/location', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 10
    assert "Chiclana de la Frontera" in [d.get("name") for d in rsp]


# Test para obtener la localidad por id
def test_getLocation(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/location/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert "Chiclana de la Frontera" == rsp.get("name")
    assert [1] == rsp.get("Player")
    assert 1 == rsp.get("region")


def test_createLocation(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post('/api/location/', headers=headers, follow_redirects=True, json={'name': 'San Fernando', 'region': 1})
    rsp = rv.get_json()

    assert "San Fernando" == rsp.get("name")
    assert 1 == rsp.get("region")
    assert [] == rsp.get("Player")
    assert 3 == rsp.get("id")


def test_updateLocation(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put('/api/location/1', headers=headers, follow_redirects=True, json={'id': 3, 'name': 'Puerto Real'})
    rsp = rv.get_json()

    assert "Puerto Real" == rsp.get("name")
    assert 1 == rsp.get("region")
    assert [] == rsp.get("Player")
    assert 1 == rsp.get("id")


def test_deleteLocation(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete("/api/location/2", headers=headers, follow_redirects=True)
    res = rv.status
    assert '204 NO CONTENT' == res


# Test para obtener los puntos de la localidad especificada
def test_getLocationPoints(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/location/points/1", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert {"Chiclana de la Frontera": 100} == rsp


# Test para obtener los puntos de todos las localidades
def test_getPointsAllLocalities(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/location/points/", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert "Chiclana de la Frontera" in [d for d in rsp]