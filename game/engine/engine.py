from game.bo.player import Player

class Game():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = []

    def add_player(self):
        player = Player(self)
        self.players.append(player)
        return player

    def remove_player(self, player):
        self.player.remove(player)
            
    def init(self):
        pass

    def quit(self):
        pass
    
    def update_player(self, player, user_input):
        player.update_state(user_input)

    def tick(self):
        for player in self.players:
            player.tick()