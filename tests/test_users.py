import pytest
from app import create_app
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


def test_prueba(client):
    rv = client.get('/')
    assert "Here is the" in rv.get_data(as_text=True)


def test_login(client):
    rv = client.post('/login', json={'username': 'selena', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/user', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 4
    assert "selena" in [d.get("username") for d in rsp]


# Test para obtener todos los usuarios
def test_getUsers(client):
    rv = client.post('/login', json={'username': 'juan', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/user', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 10
    assert "juan" in [d.get("username") for d in rsp]


# Test para obtener el usuario por id
def test_getUser(client):
    rv = client.post('/login', json={'username': 'juan', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/user/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert "juan" == rsp.get("username")
    assert 1 == rsp.get("id")
    assert "juan@a.a" == rsp.get("email")
    assert True == rsp.get("is_active")
    assert 1 == rsp.get("player")
    assert [1] == rsp.get("roles")


# Test para hacer la creación del usuario
def test_createUser(client):
    rv = client.post('/login', json={'username': 'juan', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post('/api/user/', headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert "manolo" == rsp.get("username")
    assert 7 == rsp.get("id")
    assert "juan@a.a" == rsp.get("email")
    assert True == rsp.get("is_active")
    assert None == rsp.get("player")
    assert [] == rsp.get("roles")


# Test para editar un usuario
def test_updateUser(client):
    rv = client.post('/login', json={'username': 'juan', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put('/api/user/1', headers=headers, follow_redirects=True, json={'id': 1, 'email': 'juanito@clic.com', 'username': 'juanito'})
    rsp = rv.get_json()

    assert "juanito" == rsp.get("username")
    assert 1 == rsp.get("id")
    assert "juanito@clic.com" == rsp.get("email")
    assert True == rsp.get("is_active")
    assert 1 == rsp.get("player")
    assert [1] == rsp.get("roles")


# Test para eliminar un usuario
def test_deleteUser(client):
    rv = client.post('/login', json={'username': 'juan', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete("/api/user/1", headers=headers, follow_redirects=True)
    res = rv.status
    assert '204 NO CONTENT' == res