import pytest

from flask import session


# def test_register(client):
#     # Test that we can GET the register page successfully
#     response_code = client.get('/').status_code
#     assert response_code == 200
#
#     # Test that we can register a user (POST), supplying a valid user name and password.
#     response = client.post(
#         '/authentication/register',
#         data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
#     )
#     assert response.headers['Location'] == 'http://localhost/authentication/login'

def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200

