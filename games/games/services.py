from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Genre


def get_game_list(repo: AbstractRepository):
    return repo.get_games()


def sort_games(repo: AbstractRepository, sort: str, order: str, genre=""):
    if genre != "":
        games = repo.get_games_by_genre(Genre(genre))
    else:
        games = repo.get_games()

    if sort == 'title':
        if order == 'asc':
            games.sort(key=lambda game: game.title)
        elif order == 'desc':
            games.sort(key=lambda game: game.title, reverse=True)

    if sort == 'price':
        if order == 'asc':
            games.sort(key=lambda game: game.price)
        elif order == 'desc':
            games.sort(key=lambda game: game.price, reverse=True)

    return games
