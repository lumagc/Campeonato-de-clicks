import pytest
from app import create_app
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


def test_getRegions(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/region', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 10
    assert "Cádiz" in [d.get("name") for d in rsp]


def test_getRegion(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/region/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert "Cádiz" == rsp.get("name")
    assert 1 == rsp.get("country")
    assert [1] == rsp.get("Location")


def test_createRegion(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post('/api/region/', headers=headers, follow_redirects=True, json={'name': 'Sevilla', 'country': 1})
    rsp = rv.get_json()

    assert "Sevilla" == rsp.get("name")
    assert 1 == rsp.get("country")
    assert [] == rsp.get("Location")


def test_updateRegion(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put('/api/region/1', headers=headers, follow_redirects=True, json={'id': 1, 'name': 'Sevilla'})
    rsp = rv.get_json()

    assert "Sevilla" == rsp.get("name")
    assert 1 == rsp.get("country")
    assert [1] == rsp.get("Location")


def test_deleteRegion(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete("/api/region/1", headers=headers, follow_redirects=True)
    res = rv.status
    assert '204 NO CONTENT' == res


def test_getRegionPoints(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/region/points/1", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert {"Cádiz": 100} == rsp


def test_getPointsAllRegions(client):
    rv = client.post('/login', json={'username': 'lual', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/region/points/", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert "Cádiz" in [d for d in rsp]