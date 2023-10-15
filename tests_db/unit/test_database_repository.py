from datetime import date, datetime

import pytest

from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import Publisher, Genre, Game, Review, User, make_review
from games.adapters.repository import RepositoryException


def test_repository_can_add_and_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    # creating and adding users to the db
    user = User('Messi', 'messi', 'Qwer1234')
    repo.add_user(user)
    repo.add_user(User('Haaland', 'Haaland', 'Mancity1234'))
    # test that the db can get the that was just added
    user2 = repo.get_user('messi')
    assert user2 == user and user2 is user


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('ronaldo') # the user Ronaldo does not exist in the db
    assert user is None


def test_repository_can_get_all_users(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user1 = User('Messi', 'messi', 'Qwer1234')
    user2 = User('Haaland', 'Haaland', 'Mancity1234')
    user3 = User('The Doctor', 'doctorwho', 'BadWolf42')
    repo.add_user(user1)
    repo.add_user(user2)
    repo.add_user(user3)
    all_users = repo.get_all_users()
    assert len(all_users) == 3 # the repo does not have any pre-existing users
    assert user1 in all_users
    assert user2 in all_users
    assert user3 in all_users


def test_repository_can_add_and_retrieve_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game1 = Game(123, "Five Nights at Freddy's")
    game1.price = 5.00 # game tables require a price column
    repo.add_game(game1)
    game_from_repo = repo.get_game(123)
    assert game_from_repo == game1
    game_from_csv = Game(1727670, 'Home Office Tasker')
    game_from_repo = repo.get_game(1727670)
    assert game_from_repo == game_from_csv


def test_repository_can_get_all_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    all_games = repo.get_all_games()
    real_game_from_csv = Game(7940, "Call of DutyÂ® 4: Modern WarfareÂ®")
    another_game_from_csv = Game(1624600, "Realms VR")
    assert len(all_games) == 877
    assert real_game_from_csv in all_games
    assert another_game_from_csv in all_games


def test_repository_can_retrieve_game_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    number_of_games = repo.get_number_of_games()
    assert number_of_games == 877


def test_repository_can_get_games_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre1 = Genre('Indie')
    indie_games = repo.get_games_by_genre(genre1)
    # there are 649 games tagged with Indie in the games.csv
    assert len(indie_games) == 649
    for game in indie_games:
        # checking that the Indie genre is in every game returned
        assert genre1 in game.genres


def test_repository_can_get_games_by_title_search(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    games = repo.get_games_by_title_search('fun')
    assert len(games) == 4 # there are 4 games in csv with 'fun' in the title
    assert Game(1422880, 'Frisbee For Fun') in games
    assert Game(1503530, 'Minit Fun Racer') in games
    for game in games:
        assert 'fun' in game.title.lower() # checking that all games have fun in the title


def test_repository_can_get_games_by_publisher_search(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    games = repo.get_games_by_publisher_search("sega")
    assert len(games) == 2 # there are only two games by Sega here
    assert Game(34282, "Shadow Dancer™") in games
    assert Game(546050, "Puyo Puyo™Tetris®") in games
    for game in games:
        assert 'sega' in game.publisher.publisher_name.lower()


def test_repository_can_get_games_by_description_search(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    games = repo.get_games_by_description_search("magnificent")
    assert len(games) == 6
    assert Game(435790, '10 Second Ninja X') in games
    for game in games:
        assert 'magnificent' in game.description


def test_repository_can_add_and_retrieve_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    publisher1 = Publisher('Concerned Ape') # creating a publisher to add
    repo.add_publisher(publisher1)
    publishers = repo.get_publishers() # returns a list of all publishers
    assert publisher1 in publishers


def test_repository_can_add_and_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    new_genre = Genre('Horror')
    repo.add_genre(new_genre)
    genres = repo.get_genres() # returns list of all genres
    assert new_genre in genres
    assert len(genres) == 25 # should update to include new genre too
    assert Genre('Action') in genres


def test_repository_can_add_and_retrieve_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    # repo has no prepopulated reviews
    user1 = User('Mariya', 'mako', 'PlasticLove80')
    repo.add_user(user1)
    new_review = make_review(user1, repo.get_game(435790), 5, 'great game')
    reviews = repo.get_reviews()
    assert new_review in reviews


def test_repository_can_update_user_wishlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    # repo has nothing prepopulated in the wishlist table, which is really
    # just a user games association table
    user1 = User('Mariya', 'mako', 'PlasticLove80')
    game1 = repo.get_game(435790)
    repo.add_user(user1)
    user1.add_favourite_game(game1)
    repo.update_user(user1)
    assert game1 in user1.favourite_games
    assert len(user1.favourite_games) == 1
    user1.remove_favourite_game(game1)
    repo.update_user(user1)
    assert game1 not in user1.favourite_games
    assert len(user1.favourite_games) == 0
