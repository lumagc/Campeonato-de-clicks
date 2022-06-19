import pytest
from app import create_app
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


def test_getCountries(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/country', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 10
    assert "España" in [d.get("name") for d in rsp]


def test_getCountry(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/country/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert "España" == rsp.get("name")
    assert [1] == rsp.get("Region")


def test_createCountry(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post('/api/country/', headers=headers, follow_redirects=True, json={'name': 'Italia'})
    rsp = rv.get_json()

    assert "Italia" == rsp.get("name")
    assert [] == rsp.get("Region")


def test_updateCountry(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put('/api/country/1', headers=headers, follow_redirects=True, json={'id': 1, 'name': 'Francia'})
    rsp = rv.get_json()

    assert "Francia" == rsp.get("name")
    assert [1] == rsp.get("Region")
    assert 1 == rsp.get("id")


def test_deleteCountry(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete("/api/country/1", headers=headers, follow_redirects=True)
    res = rv.status
    assert '204 NO CONTENT' == res


def test_getCountryPoints(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/country/points/1", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert {"España": 100} == rsp


# Test para obtener los puntos de todos las localidades
def test_getPointsAllCountries(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/country/points/", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert "España" in [d for d in rsp]