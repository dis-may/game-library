from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Genre


def get_sorted_game_list(repo: AbstractRepository, sort_by='id', order='asc'):
    if sort_by == 'title':
        if order == 'asc':
            return repo.get_games_by_title()
        elif order == 'desc':
            games = repo.get_games_by_title()
            games.reverse()
            return games
    elif sort_by == 'price':
        if order == 'asc':
            return repo.get_games_by_price()
        elif order == 'desc':
            games = repo.get_games_by_price()
            games.reverse()
            return games
    else:
        return repo.get_games_by_id()

# def sort_games(repo: AbstractRepository, sort: str, order: str, genre=""):
#     if genre != "":
#         games = repo.get_games_by_genre(Genre(genre))
#     else:
#         games = repo.get_games_by_id()
#
#     if sort == 'title':
#         if order == 'asc':
#             games.sort(key=lambda game: game.title)
#         elif order == 'desc':
#             games.sort(key=lambda game: game.title, reverse=True)
#
#     if sort == 'price':
#         if order == 'asc':
#             games.sort(key=lambda game: game.price)
#         elif order == 'desc':
#             games.sort(key=lambda game: game.price, reverse=True)
#
#     return games
