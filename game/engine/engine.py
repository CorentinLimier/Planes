

class Game():

    def __init__(self):
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def init(self):
        pass

    def quit(self):
        pass
