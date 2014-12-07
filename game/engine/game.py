
import pygame
from userInputFeed.userInputFeedVoid import UserInputFeedVoid
from userInputFeed.userInputFeedLocal import UserInputFeedLocal
from userInputFeed.userInputFeedNetwork import UserInputFeedNetwork
import game


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
            'plane': pygame.image.load('plane.png')
        }

        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Planes')

        self.players = []
        self.players.append(game.bo.player.Player(self, UserInputFeedVoid()))
        self.players.append(game.bo.player.Player(self, UserInputFeedLocal()))
        self.players.append(game.bo.player.Player(self, UserInputFeedNetwork()))

    def draw(self):
        self.screen.fill(self.color['white'])
        for player in self.players:
            self.screen.blit(self.img['plane'], player.plane_xy)
        pygame.display.update()

    def tick(self):
        quit = False
        for player in self.players:
            player.update_state_from_input_feed()
            if player.plane_crashed:
                quit = True

        if quit:
            return False
        else:
            self.draw()
            return True

    def init(self):
        for player in self.players:
            player.input_feed.start()

    def quit(self):
        for player in self.players:
            player.input_feed.stop()
