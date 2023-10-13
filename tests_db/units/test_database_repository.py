from datetime import date, datetime

import pytest

import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Messi', 'Qwer1234')
    repo.add_user(user)
    repo.add_user(User('Haaland', 'Mancity1234'))
    user2 = repo.get_user('Messi')
    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('Heungmin')
    assert user == User('Heungmin', 'Coys1234')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('Ronaldo')
    assert user is None


# def test_repository_can_retrieve_article_count(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#     number_of_games = repo.get_number_of_articles()
#     assert number_of_games == ...
