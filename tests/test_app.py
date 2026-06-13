from http import HTTPStatus

from fastapi_zero.schema import UserPublic


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
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }

    response = client.post('/users/', json=json)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_user(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_with_id(client, user):
    response = client.get(f'/users/{user.id}/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_read_user_with_id_http_exception(client, user):
    response = client.get('/users/-1/')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}

    response = client.get('/users/600/')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_update_user(client, user):
    json = {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }
    response = client.put('/users/1/', json=json)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_update_user_http_exception(client, user):
    json = {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }
    response = client.put('/users/-5/', json=json)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}

    response = client.put('/users/600/', json=json)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_delete_user(client, user):
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


def test_create_already_exist_username(client, user):
    json = {
        'username': user.username,
        'email': 'teste@teste.com',
        'password': 'teste',
    }

    response = client.post('/users/', json=json)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': f'User {user.username} already exist'}


def test_create_already_exist_email(client, user):
    json = {
        'username': 'teste',
        'email': user.email,
        'password': 'teste',
    }

    response = client.post('/users/', json=json)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': f'Already exist an email user: {user.email}'
    }


def test_update_already_exist_username_email(client, user):
    json = {
        'username': 'verusca',
        'email': 'verusca@gmail.com',
        'password': 'teste',
    }

    client.post('/users/', json=json)

    response = client.put(f'/users/{user.id}', json=json)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}
