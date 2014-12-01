'''
Created on 1 déc. 2014

@author: Corentin
'''

from bo.plane import Plane

class Player():
    
    def __init__(self, name):
        self.name = name
        self.plane = Plane()