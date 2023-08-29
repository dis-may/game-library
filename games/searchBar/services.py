from games.adapters.repository import AbstractRepository
from bisect import insort_left


def get_games_by_search(repo: AbstractRepository, target_name: str):
    games = repo.get_games()
    games_by_search = []

    for game in games:
        if games.name == target_name:
            insort_left(games_by_search, game)
    return games_by_search
