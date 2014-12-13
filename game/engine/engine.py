import pygame
from game.hmi.hmi import Hmi


class Game():

    def __init__(self):
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def init(self):
        pass

    def quit(self):
        pass
