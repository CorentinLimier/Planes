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
            'green': (0, 255, 0),
            'blue': (0, 0, 255)
        }
        
        self.img = {
            'plane': pygame.image.load('game/hmi/asset/plane.png')
        }

        self.screen = pygame.display.set_mode((self.game.width, self.game.height))
        pygame.display.set_caption('Planes')
        
    def rot_center(self, image, position, angle):
        """rotate an image while keeping its center"""
        rect = image.get_rect().move(*position)
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect
        
    def emptyScreen(self):        
        self.screen.fill(self.color['white'])
    
    def draw_plane(self, plane):
        plane, position = self.rot_center(self.img['plane'], plane.position, plane.angle)
        self.screen.blit(plane, position)
        #pygame.draw.circle(self.screen, self.color['black'], (int(player.plane.position[0]),int(player.plane.position[1])), 5)
        
    def draw_bullet(self, bullet):
        pygame.draw.circle(self.screen, self.color['blue'], (int(bullet.position[0]),int(bullet.position[1])), 5)

    def updateScreen(self):
        pygame.display.update()
        
    def draw(self):
        self.emptyScreen()    
        for player in self.game.players:
            for bullet in player.plane.bullets:
                self.draw_bullet(bullet)  
            self.draw_plane(player.plane)
          
        self.updateScreen()