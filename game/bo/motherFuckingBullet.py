import math

class MotherFuckingBullet():
    
    def __init__(self, position, angle, width, height):
        self.width = width
        self.height = height
        self.position = position
        self.angle = angle
        self.speed = 8
        self.crashed = False
    
    def update(self):
        self.move_forward()
    
    def move_forward(self, frameCount = 1):
        angle = math.radians(self.angle)
        self.position[0] += self.speed * frameCount * math.cos(angle)
        self.position[1] -= self.speed * frameCount * math.sin(angle)
        if  self.position > (self.width, self.height) or self.position > (self.width, self.height):
            self.crash()
        
    def crash(self):
        self.crashed = True