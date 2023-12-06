import time
import pygame
import random as rnd
import enchant
from typing import Union
import numpy as np
from network import Network
from utils import *


class Player:
    score = 0
    words = set()

    def __init__(self, name: str, color: tuple[int, int, int]):
        self.name = name
        self.color = color

    def reset(self):
        self.score = 0
        self.words.clear()


class Engine:

    def __init__(self):
        self.dictionary = enchant.Dict('en_US')
        self.letters = {'E': 0.111607,
                        'M': 0.030129,
                        'A': 0.084966,
                        'H': 0.030034,
                        'R': 0.075809,
                        'G': 0.024705,
                        'I': 0.075448,
                        'B': 0.020720,
                        'O': 0.071635,
                        'F': 0.018121,
                        'T': 0.069509,
                        'Y': 0.017779,
                        'N': 0.066544,
                        'W': 0.012899,
                        'S': 0.057351,
                        'K': 0.011016,
                        'L': 0.054893,
                        'V': 0.010074,
                        'C': 0.045388,
                        'X': 0.002902,
                        'U': 0.036308,
                        'Z': 0.002722,
                        'D': 0.033844,
                        'J': 0.001965,
                        'P': 0.031671,
                        'Q': 0.001962}
        self.dictatorium = {}
        self.status = {'grid': np.array([]),
                       'all_words': set(),
                       'words': {},
                       't0': 0,
                       'time': 0,
                       'time_left': 0,
                       'players': {}}
        self.run = False

    def start(self, size: int, game_time: float, players: list[Player]) -> None:
        """
        initializes game
        :param size: size of grid
        :param game_time: duration of game
        :param players: list of players
        :return:
        """
        self.run = True
        # self.status['players'] = {player.name: player for player in players}
        self.status = {'grid': self.generate(size),
                       'all_words': set(),
                       'words': {player.name: set() for player in players},
                       't0': time.time(),
                       'time': game_time,
                       'time_left': game_time,
                       'players': {player.name: player for player in players}}

    def update(self):
        self.status['time_left'] = max(0.0, self.status['time'] + self.status['t0'] - time.time())
        if self.status['time_left'] == 0:
            self.run = False

    def generate(self, n: int) -> np.ndarray:
        """
        generates n by n array of weighted letters
        :param n: dimension of array
        :return: n by n array
        """
        return np.array(rnd.choices(list(self.letters.keys()),
                                    list(self.letters.values()),
                                    k=n * n)).reshape((n, n))

    def value_word(self, word) -> int:
        """
        value word
        :param word: word to check
        :return: value of word
        """
        return round(sum([1 / self.letters[l] for l in word]) * len(word))

    def check_sequence(self, seq: list[tuple[int, int]], player: Player) -> None:
        """
        check to see if word defined by sequence is in the English dictionary
        :param player: player submitting word
        :param seq: integer pairs corresponding with coordinates
        :return:
        """
        if not self.run:
            return
        for coord in seq:
            if seq.count(coord) != 1:
                print('cheating detected')
                return

        for pair in make_pairs(seq):
            if not adj(*pair):
                print('cheating detected')
                return

        word = str().join([self.status['grid'][t] for t in seq])
        if self.dictionary.check(word) and word not in self.status['all_words'] and len(word) > 1:
            player.score += self.value_word(word)
            player.words.add(word)
            self.add_word(word, player)

        # return self.dictionary.check(word) and word not in self.status['words'], word

    def add_word(self, word: str, player: Player) -> None:
        """
        adds word to set of global words and set of words submitted by player
        :param word: word to be added
        :param player: player who submitted word
        :return:
        """
        self.status['all_words'].add(word)
        self.status['words'][player.name].add(word)





