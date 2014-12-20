import math

class MotherFuckingBullet():
    
    def __init__(self, position, angle, width, height):
        self.width = width
        self.height = height
        self.position = position
        self.angle = angle
        self.speed = 30
        self.crashed = False
    
    def update(self):
        self.move_forward()
    
    def move_forward(self, frameCount = 1):
        angle = math.radians(self.angle)
        self.position[0] += self.speed * frameCount * math.cos(angle)
        self.position[1] -= self.speed * frameCount * math.sin(angle)
        self.isCrashed()

        
    def isCrashed(self):
        if  self.position[0] > self.width or self.position[1] > self.height or self.position[0] < 0 or self.position[1] < 0:
            self.crashed = True