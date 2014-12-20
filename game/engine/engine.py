from game.bo.player import Player


class Game():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = []
        self.bullets = []

    def add_player(self):
        player = Player(self)
        self.players.append(player)
        return player

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)
        
    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def remove_bullet(self, bullet):
        if bullet in self.bullets:
            self.bullets.remove(bullet)

    def init(self):
        pass

    def quit(self):
        pass
    
    def update_player(self, player, user_input):
        player.update_state(user_input)

    def tick(self):
        for player in self.players:
            player.tick()

    def update(self):
        for player in self.players:
            player.plane.move_forward()
        for bullet in self.bullets:
            bullet.move_forward()
