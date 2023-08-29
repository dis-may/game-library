import pytest
from games.adapters.memory_repository import MemoryRepository, populate
from games.domainmodel.model import Game, Publisher, Genre


def test_init():
    # checking an empty memory repository first
    repo = MemoryRepository()

    # checking that the following methods work
    assert repo.get_games() == []
    assert repo.get_publishers() == []
    assert repo.get_genres() == []


def test_add_game():
    # adding a valid game
    game1 = Game(1, "Example Game")
    repo = MemoryRepository()
    assert repo.get_number_of_games() == 0
    repo.add_game(game1)
    assert len(repo.get_games()) == 1
    assert repo.get_number_of_games() == 1
    assert game1 in repo.get_games()


def test_add_publisher():
    # adding a valid publisher
    publisher1 = Publisher("Example Publisher")
    repo = MemoryRepository()
    repo.add_publisher(publisher1)
    assert len(repo.get_publishers()) == 1
    assert publisher1 in repo.get_publishers()


def test_add_genre():
    # adding a valid genre
    genre1 = Genre("Example Genre")
    repo = MemoryRepository()
    repo.add_genre(genre1)
    assert len(repo.get_genres()) == 1
    assert genre1 in repo.get_genres()


@pytest.fixture
def memory_repo():
    repo_instance = MemoryRepository()
    # populated with the real csv data
    populate(repo_instance)
    return repo_instance


def test_database_sizes(memory_repo):
    # test that they are the correct size
    assert len(memory_repo.get_games()) == 877
    assert memory_repo.get_number_of_games() == 877
    assert len(memory_repo.get_publishers()) == 798
    assert len(memory_repo.get_genres()) == 24


def test_no_duplicate_items(memory_repo):
    # set removes duplicated elements, so if there are none, they have the same size
    games = memory_repo.get_games()
    publishers = memory_repo.get_publishers()
    genres = memory_repo.get_genres()
    assert len(set(games)) == len(games)
    assert len(set(publishers)) == len(publishers)
    assert len(set(genres)) == len(genres)


def test_get_games_dataset(memory_repo):
    games = memory_repo.get_games()
    # test that games are ordered by id
    assert games == sorted(games)
    first_three_games = str(games[:3])
    # the same as the csv reader test, which is correct
    assert first_three_games == "[<Game 3010, Xpand Rally>, <Game 7940, Call of Duty® 4: Modern Warfare®>, <Game 11370, Nikopol: Secrets of the Immortals>]"


def test_get_publishers_dataset(memory_repo):
    publishers = memory_repo.get_publishers()
    # test that publishers are ordered alphabetically
    assert publishers == sorted(publishers)
    first_three_publishers = str(publishers[:3])
    assert first_three_publishers == "[<Publisher 13-lab,azimuth team>, <Publisher 2Awesome Studio>, <Publisher 2Frogs Software>]"


def test_get_genres_dataset(memory_repo):
    genres = memory_repo.get_genres()
    assert genres == sorted(genres)
    first_three_genres = str(genres[:3])
    assert first_three_genres == "[<Genre Action>, <Genre Adventure>, <Genre Animation & Modeling>]"


def test_get_game_by_id(memory_repo):
    # test for valid game
    game1 = memory_repo.get_game(1671200)
    assert str(game1) == "<Game 1671200, Honkai Impact 3rd>"
    # test for invalid game
    game2 = memory_repo.get_game(0)
    assert game2 is None


def test_get_games_by_genre(memory_repo):
    # checking a valid genre
    genre1 = Genre("Action")
    action_games = memory_repo.get_games_by_genre(genre1)
    # finish this LATER pls

# write more tests for search functionality!!
