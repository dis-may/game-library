from bisect import insort_left
from typing import List
import os

from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Publisher


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = []
        self.__publishers = []
        self.__genres = []

    def add_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self.__games, game)  # games are ordered by game id

    def get_games_by_id(self) -> List[Game]:
        return self.__games

    def get_game(self, game_id: int) -> Game:
        for game in self.__games:
            if game.game_id == game_id:
                return game

    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        game_list = []
        for game in self.__games:
            if genre in game.genres:
                game_list.append(game)

        return game_list

    def get_games_by_title_search(self, query: str) -> List[Game]:
        games_that_match = []
        for game in self.__games:
            if query in game.title.lower():
                games_that_match.append(game)
        return games_that_match

    def get_games_by_publisher_search(self, query: str) -> List[Game]:
        games_that_match = []
        for game in self.__games:
            if query in game.publisher.publisher_name.lower():
                games_that_match.append(game)
        return games_that_match

    def get_games_by_description_search(self, query: str) -> List[Game]:
        games_that_match = []
        for game in self.__games:
            if game.description is not None:
                if query in game.description.lower():
                    games_that_match.append(game)
        return games_that_match

    def get_number_of_games(self) -> int:
        return len(self.__games)

    def add_publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            insort_left(self.__publishers, publisher)

    def get_publishers(self) -> List[Publisher]:
        return self.__publishers

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre):
            insort_left(self.__genres, genre)

    def get_genres(self):
        return self.__genres


def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(dir_name, "data/games.csv")
    reader = GameFileCSVReader(games_file_name)

    reader.read_csv_file()

    games = reader.dataset_of_games

    for game in games:
        repo.add_game(game)

    genres = reader.dataset_of_genres

    for genre in genres:
        repo.add_genre(genre)

    publishers = reader.dataset_of_publishers

    for pub in publishers:
        repo.add_publisher(pub)


