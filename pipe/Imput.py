'''
Created on 30 nov. 2014

@author: Corentin
'''

from collections import deque

class Input(object):

    def __init__(self):
        self.inputs = deque()
        
    def push(self, element):
        self.inputs.append(element)
        
    def pop(self):
        return self.inputs.pop()

        