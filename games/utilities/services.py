from games.adapters.repository import AbstractRepository


def get_genre_names(repo: AbstractRepository):
    genre_list = repo.get_genres()
    return [genre.genre_name for genre in genre_list]
