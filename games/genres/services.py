from games.adapters.repository import AbstractRepository


def get_list_of_genres(repo: AbstractRepository):
    return repo.get_genres()


def get_games_by_genre(repo: AbstractRepository, genre):
    return repo.get_games_by_genre(genre)

