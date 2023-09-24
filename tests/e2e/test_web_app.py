import pytest

from flask import session


def test_register(client):
    # Test that we can GET the register page successfully
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Test that we can register a user (POST), supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'
