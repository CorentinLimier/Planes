from game.bo.player import Player
from game.bo.plane import Plane


class Game():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = []
        self.bullets = []

    def add_player(self):
        plane = Plane(self.width, self.height)
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

    
    def check_bullets(self):
        for player in self.players:
            
            for bullet in player.plane.bullets:
                
                for opponent in self.players:
                    if opponent is player : 
                        continue
                    
                    if ((bullet.position[0] - opponent.plane.position[0] > 0) and 
                        (bullet.position[0] - opponent.plane.position[0] < 60) and
                        (bullet.position[1] - opponent.plane.position[0] > 0) and
                        (bullet.position[0] - opponent.plane.position[0] < 45)):
                            bullet.crashed = True
                            opponent.plane.hearts -= 10
                            
    def check_players(self):
        for player in self.players:
            if player.plane.crashed:
                plane = Plane(self.width, self.height)
                player.plane = plane
    
    def tick(self):
        for player in self.players:
            self.check_players()
            self.check_bullets()
            player.update()
            
    