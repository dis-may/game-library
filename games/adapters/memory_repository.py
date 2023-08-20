from bisect import insort_left
from typing import List
import os

from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = []

    def add_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self.__games, game)  # games are ordered by game id

    def get_games(self) -> List[Game]:
        return self.__games

    def get_number_of_games(self) -> int:
        return len(self.__games)
