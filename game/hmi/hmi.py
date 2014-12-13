'''
Created on 1 dec. 2014

@author: Corentin
'''

import pygame

class Hmi():
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = []

        self.color = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'blue': (0, 255, 0),
            'green': (0, 0, 255)
        }
        
        self.img = {
            'plane': pygame.image.load('game/hmi/asset/plane.png')
        }

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Planes')
        
    def add_player(self, player):
        self.players.append(player)        

    def remove_player(self, player):
        self.players.remove(player)

    def emptyScreen(self):        
        self.screen.fill(self.color['white'])
    
    def updatePlayer(self, player):
        self.screen.blit(pygame.transform.rotate(self.img['plane'], player.plane.angle), player.plane.position)
        
    def updateScreen(self):
        pygame.display.update()
        
    def draw(self):
        self.emptyScreen()
        for player in self.players:
            self.updatePlayer(player)
        self.updateScreen()