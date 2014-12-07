'''
Created on 1 d�c. 2014

@author: Corentin
'''

from game.hmi.hmi import Hmi

class Game():
    
    def __init__(self, nb_players, height, width):
        self.nb_players = nb_players
        self.hmi = Hmi(height, width)
        