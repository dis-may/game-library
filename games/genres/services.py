from games.adapters.repository import AbstractRepository
from games.games.services import get_sorted_game_list
from bisect import insort_left


def get_list_of_genres(repo: AbstractRepository):
    return repo.get_genres()


def get_sorted_games_by_genre(repo: AbstractRepository, target_genre: str, sort='id', order='asc'):
    game_list = get_sorted_game_list(repo, sort, order)
    games_with_genre = []
    for game in game_list:
        for genre in game.genres:
            if genre.genre_name == target_genre:
                games_with_genre.append(game)

    return games_with_genre
