'''
Created on 30 nov. 2014

@author: Corentin
'''

class InputAction():
    
    def __init__(self):
        self.turnLeft = False
        self.turnRight = False
        self.fire = False
        
    def updateStatus(self):
        raise NotImplementedError
        