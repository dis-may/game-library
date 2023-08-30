from games.adapters.repository import AbstractRepository
from bisect import insort_left


def get_list_of_genres(repo: AbstractRepository):
    return repo.get_genres()


def get_games_by_genre_name(repo: AbstractRepository, target_name: str):
    games = repo.get_games_by_id()
    games_by_genre = []
    for game in games:
        for genre in game.genres:
            if genre.genre_name == target_name:
                insort_left(games_by_genre, game)

    return games_by_genre
