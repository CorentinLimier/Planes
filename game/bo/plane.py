'''
Created on 1 d�c. 2014

@author: Corentin
'''

from game.physicsEngine.position import Position

class Plane():
    
    def __init__(self):
        self.position = Position()
        self.angle = 0
        
    def update(self, elapsed_time = 1):
        pass