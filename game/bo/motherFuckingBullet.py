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
    
    def move_forward(self, frame_count = 1):
        angle = math.radians(self.angle)
        self.position[0] += self.speed * frame_count * math.cos(angle)
        self.position[1] -= self.speed * frame_count * math.sin(angle)
        self.update_crashed()

        
    def update_crashed(self):
        if  self.position[0] > self.width or self.position[1] > self.height or self.position[0] < 0 or self.position[1] < 0:
            self.crashed = True
        if  self.position > (self.width, self.height) or self.position > (self.width, self.height):
            self.crash()
        
    def crash(self):
        self.crashed = True