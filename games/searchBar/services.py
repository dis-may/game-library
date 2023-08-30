from games.adapters.repository import AbstractRepository
from bisect import insort_left


def get_games_by_search(repo: AbstractRepository, target_name: str):
    games = repo.get_games_by_id()
    games_by_search = []

    for game in games:
        if target_name in game.title.lower():
            insort_left(games_by_search, game)
    return games_by_search

def get_games_by_publisher(repo: AbstractRepository, target_name: str):
    games = repo.get_games_by_id()
    games_by_publisher = []

    for game in games:
        if target_name in game.publisher.publisher_name.lower():
            insort_left(games_by_publisher, game)
    return games_by_publisher

def get_games_by_description(repo: AbstractRepository, target_name: str):
    games = repo.get_games_by_id()
    games_by_description = []

    for game in games:
        if game.description is not None:
            if target_name in game.description.lower():
                insort_left(games_by_description, game)
    return games_by_description

