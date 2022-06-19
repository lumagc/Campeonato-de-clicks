import pytest
from app import create_app
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


# Test para obtener todos los jugadores
def test_getTeams(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/team', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 10
    assert "Rotísimos" in [d.get("name") for d in rsp]


# Test para obtener el jugador por id
def test_getTeam(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/team/2', headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert "Rotísimos" == rsp.get("name")
    assert 2 == rsp.get("id")


def test_createTeam(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post('/api/team/', headers=headers, follow_redirects=True, json={'name': 'La joda'})
    rsp = rv.get_json()

    assert "La joda" == rsp.get("name")


def test_updateTeam(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put('/api/team/2', headers=headers, follow_redirects=True, json={'id': 2, 'name': 'Los mejores'})
    rsp = rv.get_json()

    assert "Los mejores" == rsp.get("name")
    assert 2 == rsp.get("id")


def test_deleteTeam(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete("/api/team/2", headers=headers, follow_redirects=True)
    res = rv.status
    assert '204 NO CONTENT' == res


# Test para obtener los puntos del jugador especificado
def test_getTeamsPoints(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/team/points/2", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert {'Rotísimos': 100} == rsp


# Test para obtener los puntos de todos los jugadores
def test_getPointsAllTeams(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/team/points/", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert 'Rótisimos' in [d for d in rsp]
