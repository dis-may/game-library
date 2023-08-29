import pytest
from games.adapters.memory_repository import MemoryRepository, populate
from games.domainmodel.model import Game, Publisher, Genre


@pytest.fixture
def memory_repo():
    repo_instance = MemoryRepository()
    populate(repo_instance)
    return repo_instance


def test_add_game(memory_repo):
    game1 = Game(1, "Example Game 1")
    memory_repo.add_game(game1)
    assert game1 in memory_repo.get_games()
