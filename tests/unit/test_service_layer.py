import pytest
import games.adapters.repository as repo
from games.adapters.memory_repository import MemoryRepository, populate
from games.gameDescription import services as game_services
from games.genres import services as genre_services
from games.searchBar import services as search_services


@pytest.fixture
def memory_repo():
    repo_instance = MemoryRepository()
    # populated with the real csv data
    populate(repo_instance)
    return repo_instance


# test service layer returns an existing game object
def test_can_get_existing_game(memory_repo):
    game = game_services.get_game(12140, memory_repo)

    assert game.title == "Max Payne"
    assert game.game_id == 12140
    assert game.description == "Max Payne is a man with nothing to lose in the violent, cold urban night. A fugitive undercover cop framed for murder, hunted by cops and the mob, Max is a man with his back against the wall, fighting a battle he cannot hope to win. Max Payne is a relentless story-driven game about a man on the edge, fighting to clear his name while struggling to uncover the truth about his slain family amongst a myriad of plot-twists and twisted thugs in the gritty bowels of New York during the century's worst blizzard. The groundbreaking original cinematic action-shooter, Max Payne introduced the concept of Bullet Time® in videogames. Through its stylish slow-motion gunplay combined with a dark and twisted story, Max Payne redefined the action-shooter genre."
    assert game.image_url == "https://cdn.akamai.steamstatic.com/steam/apps/12140/header.jpg?t=1618852800"
    assert game.price == 3.49
    assert game.release_date == "Jan 6, 2011"
    # idk how to assert publisher or genres :(



