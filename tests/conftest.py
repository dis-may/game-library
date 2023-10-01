import pytest

from games import create_app
from games.adapters.repository_populate import populate
from games.adapters.memory_repository import MemoryRepository


# no testing data, using real data for testing so the path is the same
@pytest.fixture
def memory_repo():
    repo_instance = MemoryRepository()
    # populated with the real csv data
    populate(repo_instance)
    return repo_instance


# @pytest.fixture
# def client():
#     my_app = create_app({
#         'TESTING': True,
#         'WTF_CSRF_ENABLED': False,
#         'SESSION_COOKIE_SECURE': False,  # Disable secure cookies for testing
#         'SESSION_COOKIE_HTTPONLY': True,  # Enable httpOnly cookies
#     })
#
#     return my_app.test_client()

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SESSION_COOKIE_SECURE': False,  # Disable secure cookies for testing
        'SESSION_COOKIE_HTTPONLY': True,  # Enable httpOnly cookies
    })

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def register(self, name='Alice', user_name='alice123', password='Wonderland123'):
        return self.__client.post(
            'authentication/register',
            data={'name': name, 'user_name': user_name, 'password': password}
        )

    def login(self, user_name='alice123', password='Wonderland123'):
        return self.__client.post(
            'authentication/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
