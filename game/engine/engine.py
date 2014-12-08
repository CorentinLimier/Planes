
import pygame


class Game():

    def __init__(self):
        self.display_width = 800
        self.display_height = 400

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

        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Planes')

        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def draw(self):
        self.screen.fill(self.color['white'])
        for player in self.players:
            self.screen.blit(self.img['plane'], player.plane_xy)
        pygame.display.update()

    def init(self):
        pass

    def quit(self):
        pass
