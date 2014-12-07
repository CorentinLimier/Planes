

from game.physicsEngine.position import Position

class Plane():
    
    def __init__(self):
        self.position = Position()
        self.angle = 0
        
    def update(self, elapsed_time = 1):
        pass