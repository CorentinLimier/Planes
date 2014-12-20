import math

class Plane():
    
    def __init__(self, game):
        self.game = game
        self.position = [self.game.width * 0.45, self.game.height * 0.8]
        self.angle = 0
        self.rotation_speed = 5
        self.speed = 5
        self.crashed = False
        
    def turn_left(self, frameCount = 1):
        self.angle += self.rotation_speed
    
    def turn_right(self, frameCount = 1):
        self.angle -= self.rotation_speed
        
    def move_forward(self, frameCount = 1):
        angle = math.radians(self.angle)
        self.position[0] += self.speed * frameCount * math.cos(angle)
        self.position[0] %= self.game.width
        self.position[1] -= self.speed * frameCount * math.sin(angle)
        
    def crash(self):
        self.crashed = True
        

        