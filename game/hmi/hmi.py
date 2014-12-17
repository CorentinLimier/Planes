'''
Created on 1 dec. 2014

@author: Corentin
'''

import pygame, math

class Hmi():
    
    def __init__(self, game):
        self.game = game

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

        self.screen = pygame.display.set_mode((self.game.width, self.game.height))
        pygame.display.set_caption('Planes')
        
    def emptyScreen(self):        
        self.screen.fill(self.color['white'])
    
    def updatePlayer(self, player):
        self.screen.blit(pygame.transform.rotate(self.img['plane'], player.plane.angle), player.plane.position)
        pygame.draw.circle(self.screen, self.color['black'], (int(player.plane.position[0]),int(player.plane.position[1])), 5)
        
    def updateScreen(self):
        pygame.display.update()
        
    def draw(self):
        self.emptyScreen()
        for player in self.game.players:
            self.updatePlayer(player)
        self.updateScreen()