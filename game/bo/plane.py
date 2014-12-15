class Plane():
    
    def __init__(self, game):
        self.game = game
        self.position = (self.game.width * 0.45, self.game.height * 0.8)
        self.angle = 0
        self.crashed = False
        
    def turn_left(self, frameCount = 1):
        self.position = self.position[0], (self.position[1] + 5 * frameCount)
    
    def turn_right(self, frameCount = 1):
        self.position = self.position[0], self.position[1] - 5 * frameCount
        
    def move_forward(self, frameCount = 1):
        self.position = (self.position[0] +  1 * frameCount) % self.game.width, self.position[1]
        
    def crash(self):
        self.crashed = True
        

        