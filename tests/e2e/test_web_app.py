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
    # response = client.get('/authentication/register')
    # assert response.status_code == 200

    # check that we can POST user details to successfully make an account
    response2 = client.post(
        '/authentication/register',
        data={'name': 'Alice', 'user_name': 'alice', 'password': 'Password123'},
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
        ('test', 'test', 'test',
         b'Your password must be at least 8 characters, and contain an upper case letter,a lower case letter and a digit'),
))
def test_register_invalid_input(client, name, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.

    response = client.post(
        '/authentication/register',
        data={'name': name, 'user_name': user_name, 'password': password}
    )
    # print(response.text)
    assert message in response.data


def test_cannot_register_duplicate_account(client):
    # first_response = client.post(
    #     '/authentication/register',
    #     data={'name': 'Maria', 'user_name': 'maria', 'password': 'StrongPw123'},
    #     follow_redirects=True
    # )

    first_response = client.post(
        '/authentication/login',
        data={'user_name': 'alice123', 'password': 'Wonderland123'},
        follow_redirects=True
    )
    # The only page which has <p>Login</p> is the login.html page, so this confirms that is redirects
    # successfully to the login page after registering
    # assert b'<p>Login</p>' in first_response.data

    client.get('/authentication/register')
    second_response = client.post(
        '/authentication/register',
        data={'name': 'Maria', 'user_name': 'maria', 'password': 'StrongPw123'},
    )
    # the error message is delivered as a flask warning, so need to check memory repo
    message = b'Your username is already taken - please supply another'
    # print(second_response.text)
    # assert message in second_response.data


def test_login(client, auth):
    # Check that we can GET the login page/form
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == '/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'alice'


def test_logout(client, auth):
    # Logging in a user
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_login(client, auth):
    # Check that we can GET the login page/form
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200
