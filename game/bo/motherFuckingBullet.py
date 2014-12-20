import math

class MotherFuckingBullet():
    
    def __init__(self, game, player):
        self.game = game,
        self.player = player
        self.position = [player.plane.position[0] + 60, player.plane.position[1] + 20]
        self.angle = player.plane.angle
        self.speed = 8
    
    def move_forward(self, frameCount = 1):
        angle = math.radians(self.angle)
        self.position[0] += self.speed * frameCount * math.cos(angle)
        self.position[1] -= self.speed * frameCount * math.sin(angle)        