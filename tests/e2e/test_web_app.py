import pytest

from flask import session


def test_home(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'My Game Library' in response.data


def test_games_page(client):
    response = client.get('/games')
    assert response.status_code == 200
    assert b'All Games' in response.data


def test_register(client):
    # check that we can GET the register page in order to enter details
    response = client.get('/authentication/register')
    assert response.status_code == 200

    # check that we can POST user details to successfully make an account
    response = client.post(
        '/authentication/register',
        data={'name': 'Alice', 'user_name': 'al', 'password': 'Password123'},
    )
    response = client.post(
        '/authentication/login',
        data={'user_name': 'alice123', 'password': 'Wonderland123'},
        follow_redirects=True
    )
    # The only page which has <p>Login</p> is the login.html page, so this confirms that is redirects
    # successfully to the login page after registering
    assert b'<p>Login</p>' in response.data


@pytest.mark.parametrize(('name', 'user_name', 'password', 'message'), (
        (None, '', '', b'Your name is required'),
        ('a', '', '', b'Your name is too short'),
        ('Annie', 'a', '', b'Your user name is too short'),
        ('longer name', 'username1', '', b'Your password is required'),
('test', 'test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,a lower case letter and a digit'),
        # ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_invalid_input(client, name, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'name': name, 'user_name': user_name, 'password': password}
    )
    assert message in response.data
