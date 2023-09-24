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
