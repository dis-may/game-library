import pytest
from games.domainmodel.model import Genre, User, Game, Publisher, Review, Wishlist


from games.games import services as games_services
from games.gameDescription import services as game_description_services
from games.genres import services as genre_services
from games.searchBar import services as search_services
from games.wishlist import services as wishlist_services
from games.authentication import services as auth_services


# test game description service layer returns an existing game object
def test_can_get_existing_game(memory_repo):
    game_from_services = game_description_services.get_game(12140, memory_repo)
    game_from_repo = memory_repo.get_game(12140)

    assert game_from_services.title == "Max Payne"
    assert game_from_services.game_id == 12140
    assert game_from_services.description == "Max Payne is a man with nothing to lose in the violent, cold urban night. A fugitive undercover cop framed for murder, hunted by cops and the mob, Max is a man with his back against the wall, fighting a battle he cannot hope to win. Max Payne is a relentless story-driven game about a man on the edge, fighting to clear his name while struggling to uncover the truth about his slain family amongst a myriad of plot-twists and twisted thugs in the gritty bowels of New York during the century's worst blizzard. The groundbreaking original cinematic action-shooter, Max Payne introduced the concept of Bullet Time® in videogames. Through its stylish slow-motion gunplay combined with a dark and twisted story, Max Payne redefined the action-shooter genre."
    assert game_from_services.image_url == "https://cdn.akamai.steamstatic.com/steam/apps/12140/header.jpg?t=1618852800"
    assert game_from_services.price == 3.49
    assert game_from_services.release_date == "Jan 6, 2011"
    assert game_from_services == game_from_repo


def test_sort_by_id_games_list(memory_repo):
    # test that games are sorted by id when fetched (browsing all games, using utility sorting function)
    sorted_id_games_list = games_services.get_sorted_game_list(memory_repo)
    assert len(sorted_id_games_list) == memory_repo.get_number_of_games()
    previous_id = sorted_id_games_list[0].game_id
    for game in sorted_id_games_list:
        current_id = game.game_id
        assert previous_id <= current_id
        previous_id = current_id


def test_sort_by_title_games_list(memory_repo):
    # test that games are sorted by title when fetched (still browsing all games)
    sorted_title_games_list = games_services.get_sorted_game_list(memory_repo, 'title', 'asc')
    assert len(sorted_title_games_list) == memory_repo.get_number_of_games()
    previous_title = sorted_title_games_list[0].title
    for game in sorted_title_games_list:
        current_title = game.title
        assert previous_title <= current_title
        previous_title = current_title

        # test that the descending order works, should be == to the asc but reversed
    sorted_reversed_title_games_list = games_services.get_sorted_game_list(memory_repo, 'title', 'desc')
    sorted_reversed_title_games_list.reverse()
    assert sorted_reversed_title_games_list == sorted_title_games_list


def test_sort_by_price_games_list(memory_repo):
    # test that games are sorted by price when fetched (browsing all games)
    sorted_price_games_list = games_services.get_sorted_game_list(memory_repo, 'price', 'asc')
    assert len(sorted_price_games_list) == memory_repo.get_number_of_games()
    previous_price = sorted_price_games_list[0].price
    for game in sorted_price_games_list:
        current_price = game.price
        assert previous_price <= current_price
        previous_price = current_price

    # test that descending order works
    sorted_reversed_price_games_list = games_services.get_sorted_game_list(memory_repo, 'price', 'desc')

    previous_price = sorted_reversed_price_games_list[0].price
    for game in sorted_reversed_price_games_list:
        current_price = game.price
        assert previous_price >= current_price
        previous_price = current_price


def test_get_games_by_genre(memory_repo):
    genre_name = 'Action'
    genre = Genre('Action')
    games = genre_services.get_sorted_games_by_genre(memory_repo, genre_name)
    assert len(games) == 380
    for game in games:
        assert genre in game.genres


def test_get_games_by_title(memory_repo):
    query1 = "max"
    games_list1 = search_services.get_games_by_title(memory_repo, query1)
    # testing against a game string ensures the correct number of games and correct game objects
    game_string = "[<Game 12140, Max Payne>, <Game 1470790, Doug Flutie's Maximum Football 2020>]"
    assert str(games_list1) == game_string
    # test no case sensitivity
    query2 = "MAX"
    games_list2 = search_services.get_games_by_title(memory_repo, query2)
    assert str(games_list2) == game_string


def test_get_games_by_publisher(memory_repo):
    query1 = "sega"
    games_list1 = search_services.get_games_by_publisher(memory_repo, query1)
    game_string = "[<Game 34282, Shadow Dancer™>, <Game 546050, Puyo Puyo™Tetris®>]"
    assert str(games_list1) == game_string
    for game in games_list1:
        assert "sega" in game.publisher.publisher_name.lower()
    # test no case sensitivity
    games_list2 = search_services.get_games_by_publisher(memory_repo, "SEga")
    assert str(games_list2) == game_string


def test_get_games_by_description(memory_repo):
    query1 = "flavour"
    games_list1 = search_services.get_games_by_description(memory_repo, query1)
    game_string = "[<Game 437530, A Blind Legend>, <Game 1303170, MelDEV Power Boat Racing>]"
    assert str(games_list1 == game_string)
    for game in games_list1:
        assert query1.lower() in game.description.lower()
    # test no case sensitivity
    query2 = "FLAVOUR"
    games_list2 = search_services.get_games_by_description(memory_repo, query2)
    assert str(games_list2) == game_string


def test_can_add_to_wishlist(memory_repo):
    # test that a game can be added to a user's wishlist
    game_id = 3010
    username = 'harry'

    # Create a new user and add it to the repository
    new_user = User('Harry', username, 'Password123')
    memory_repo.add_user(new_user)

    wishlist_services.add_to_wishlist(game_id, username, memory_repo)

    # Get the user's wishlist from the repository
    user = memory_repo.get_user(username)

    assert len(user.favourite_games) == 1
    assert user.favourite_games[0].game_id == game_id


def test_can_remove_from_wishlist(memory_repo):
    # test that a game can be removed from a user's wishlist
    game_id = 3010
    username = 'harry'

    # Create a new user and add it to the repository
    new_user = User('Harry', username, 'Password123')
    memory_repo.add_user(new_user)
    # Add a game to the user's wishlist
    wishlist_services.add_to_wishlist(game_id, username, memory_repo)
    # Remove the game from the user's wishlist
    wishlist_services.remove_from_wishlist(game_id, username, memory_repo)
    # Get the user's wishlist from the repository
    user = memory_repo.get_user(username)
    # Check that the wishlist is empty
    assert len(user.favourite_games) == 0


def test_can_get_wishlist(memory_repo):
    username = 'harry'
    new_user = User('Harry', username, 'Password123')
    memory_repo.add_user(new_user)
    user = memory_repo.get_user(username)
    wishlist_services.add_to_wishlist(3010, username, memory_repo)
    user_favourite_games = user.favourite_games
    expected_result = "<Game 3010, Xpand Rally>"
    assert str(user_favourite_games[0]) == expected_result


def test_can_get_sorted_game_list(memory_repo):
    sorted_id_games_list = games_services.get_sorted_game_list(memory_repo)
    assert len(sorted_id_games_list) == memory_repo.get_number_of_games()
    previous_id = sorted_id_games_list[0].game_id
    for game in sorted_id_games_list:
        current_id = game.game_id
        assert previous_id <= current_id
        previous_id = current_id
