import pytest
from app import create_app
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


# Test para obtener todos los jugadores
def test_getPlayers(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/player', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 10
    assert "lual" in [d.get("username") for d in rsp]


# Test para obtener el jugador por id
def test_getPlayer(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/player/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert "lual" == rsp.get("username")
    assert 5 == rsp.get("user")
    assert 0 == rsp.get("points")
    assert 1 == rsp.get("location")
    assert [1] == rsp.get("teams")


def test_createPlayer(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post('/api/player/', headers=headers, follow_redirects=True,
                    json={'username': 'juancito', 'user': 1, 'points': 30, 'location': 1, 'teams': [1, 2]})
    rsp = rv.get_json()

    assert "juancito" == rsp.get("username")
    assert 1 == rsp.get("user")
    assert 30 == rsp.get("points")
    assert 1 == rsp.get("location")
    assert [1, 2] == rsp.get("teams")


def test_updatePlayer(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put('/api/player/3', headers=headers, follow_redirects=True,
                    json={'id': 3, 'username': 'el juan', 'points': 50, 'location': 1, 'teams': [1, 2]})
    rsp = rv.get_json()

    assert "lual" == rsp.get("username")
    assert 1 == rsp.get("user")
    assert 50 == rsp.get("points")
    assert 1 == rsp.get("location")
    assert [1, 2] == rsp.get("teams")


def test_deletePlayer(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete("/api/player/3", headers=headers, follow_redirects=True)
    res = rv.status
    assert '204 NO CONTENT' == res


# Test para obtener los puntos del jugador especificado
def test_getPlayerPoints(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/player/points/1", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert 0 == rsp


# Test para obtener los puntos de todos los jugadores
def test_getPointsAllPlayers(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/player/points/", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert {'id': 1, 'points': 100, 'username': 'lual'} in [d for d in rsp]
