class Plane():
    
    def __init__(self, position, angle):
        self.position = position
        self.angle = angle
        self.crashed = False
        
    def update(self, elapsed_time = 1):
        pass