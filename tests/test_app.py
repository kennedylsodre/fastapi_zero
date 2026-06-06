from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_hello_world():
    client = TestClient(app)

    response = client.get('/')

    assert response.json() == {'message': 'Hello world!'}
    assert response.status_code == HTTPStatus.OK


def test_root_hello_world_html():
    client = TestClient(app)

    response = client.get('/hello_world_html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1>Hello World!</h1>' in response.text
