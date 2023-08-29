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
    repo.add_game(game1)
    assert len(repo.get_games()) == 1
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


def test_populate():
    repo = MemoryRepository()
    populate(repo)  # populate repo with real csv data
    assert repo.get_games() != []
    assert repo.get_publishers() != []
    assert repo.get_genres() != []


@pytest.fixture
def memory_repo():
    repo_instance = MemoryRepository()
    populate(repo_instance)
    return repo_instance


def test_get_games(memory_repo):
    pass


def test_add_valid_game(memory_repo):
    game1 = Game(1, "Example Game 1")
    memory_repo.add_game(game1)
    assert game1 in memory_repo.get_games()


def test_add_invalid_game(memory_repo):
    invalid_game = "Invalid Game"
    memory_repo.add_game(invalid_game)
    assert invalid_game not in memory_repo.get_games()
