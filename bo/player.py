'''
Created on 1 d�c. 2014

@author: Corentin
'''

from game.bo.plane import Plane

class Player():
    
    def __init__(self, name):
        self.name = name
        self.plane = Plane()