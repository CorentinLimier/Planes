from game.bo.player import Player
from game.bo.plane import Plane


class Game():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = []
        self.bullets = []

    def add_player(self, position=None):
        if position is None:
            position = [self.width * 0.45, self.height * 0.8]

        plane = Plane(self.width, self.height, position)
        player = Player(plane)
        self.players.append(player)
        return player

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)
        
    def init(self):
        pass

    def quit(self):
        pass
    
    def update_player(self, player, user_input):
        player.update_state(user_input)

    def tick(self):
        for player in self.players:
            player.update()
            print player.get_position(), player.plane.angle, player.plane.crashed, player.plane.speed