from games.adapters.repository import AbstractRepository
from games.games.services import get_sorted_game_list
from bisect import insort_left


def get_games_by_title(repo: AbstractRepository, target_name: str, sort="id", order="asc"):
    games = get_sorted_game_list(repo, sort, order)
    games_by_search = []

    for game in games:
        if target_name in game.title.lower():
            games_by_search.append(game)
    return games_by_search


def get_games_by_publisher(repo: AbstractRepository, target_name: str, sort="id", order="asc"):
    games = get_sorted_game_list(repo, sort, order)
    games_by_publisher = []

    for game in games:
        if target_name in game.publisher.publisher_name.lower():
            games_by_publisher.append(game)
    return games_by_publisher


def get_games_by_description(repo: AbstractRepository, target_name: str, sort="id", order="asc"):
    games = get_sorted_game_list(repo, sort, order)
    games_by_description = []

    for game in games:
        if game.description is not None:
            if target_name in game.description.lower():
                games_by_description.append(game)
    return games_by_description
