from http import HTTPStatus


def test_root_hello_world(client):

    response = client.get('/')

    assert response.json() == {'message': 'Hello world!'}
    assert response.status_code == HTTPStatus.OK


def test_root_hello_world_html(client):

    response = client.get('/hello_world_html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1>Hello World!</h1>' in response.text


def test_create_user(client):

    json = {
        'user': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
        'id': 1,
    }

    response = client.post('/users/', json=json)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'user': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_user(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'user': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }


def test_read_user_with_id(client):
    response = client.get('/users/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_user_with_id_http_exception(client):
    response = client.get('/users/-1/')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}

    response = client.get('/users/600/')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_update_user(client):
    json = {
        'user': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }
    response = client.put('/users/1/', json=json)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_update_user_http_exception(client):
    json = {
        'user': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }
    response = client.put('/users/-5/', json=json)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}

    response = client.put('/users/600/', json=json)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_delete_user(client):
    response = client.delete('/users/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_http_exception(client):
    response = client.delete('/users/-1/')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}

    response = client.delete('/users/600/')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}
