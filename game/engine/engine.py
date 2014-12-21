from game.bo.player import Player
from game.bo.plane import Plane
import copy

class Game():
    fps = 30
    width = 800
    height = 400
    default_position = None

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = {}
        Game.default_position = [Game.width * 0.45, Game.height * 0.8]

    def get_default_position(self):
        return copy.copy(Game.default_position)

    def add_player(self, user_id):
        plane = Plane(self.width, self.height, self.get_default_position())
        player = Player(user_id, plane)
        self.players[user_id] = player
        return player

    def remove_player(self, user_id):
        del self.players[user_id]

    def get_player(self, user_id):
        return self.players[user_id]

    def init(self):
        pass

    def quit(self):
        pass

    def apply_user_input_to_player(self, user_id, user_input):
        self.players[user_id].update_state(user_input)

    def check_bullets(self):
        for user_id, player in self.players.iteritems():

            for bullet in player.plane.bullets:

                for opponent_user_id, opponent in self.players.iteritems():
                    if opponent is player:
                        continue

                    if (
                        (bullet.position[0] - opponent.plane.position[0] > 0) and
                        (bullet.position[0] - opponent.plane.position[0] < 60) and
                        (bullet.position[1] - opponent.plane.position[1] > 0) and
                        (bullet.position[1] - opponent.plane.position[1] < 45)
                    ):
                        bullet.crashed = True
                        opponent.plane.hearts -= 10

    def check_players(self):
        for user_id, player in self.players.iteritems():
            if player.plane.crashed:
                self.remove_player(user_id)
                self.add_player(user_id)

    def tick(self):
        for user_id, player in self.players.iteritems():
            self.check_players()
            self.check_bullets()
            player.update()
