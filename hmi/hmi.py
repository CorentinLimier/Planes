'''
Created on 1 déc. 2014

@author: Corentin
'''

import Tkinter as tk

class Hmi():
    
    def __init__(self, width, height):
        self.master = tk.Tk()
        self.canvas = tk.Canvas(self.master, width = width, height = height)