import math, copy
from game.bo.motherFuckingBullet import MotherFuckingBullet

class Plane():
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = [self.width * 0.45, self.height * 0.8]
        self.angle = 0
        self.rotation_speed = 5
        self.speed = 5
        self.crashed = False
        self.bullets = []
        
    def turn_left(self, frameCount = 1):
        self.angle += self.rotation_speed
    
    def turn_right(self, frameCount = 1):
        self.angle -= self.rotation_speed
        
    def update(self):
        crashed_bullets = []
        for bullet in self.bullets:
            if bullet.crashed :
                crashed_bullets.append(bullet)
            else :
                bullet.update()
        for bullet in crashed_bullets : 
            self.bullets.remove(bullet)
        self.move_forward()
        
        
    def move_forward(self, frameCount = 1):
        angle = math.radians(self.angle)
        self.position[0] += self.speed * frameCount * math.cos(angle)
        self.position[0] %= self.width
        self.position[1] -= self.speed * frameCount * math.sin(angle)
        if  self.position > (self.width, self.height) or self.position > (self.width, self.height):
            self.crash()
        
    def shoot(self):
        bullet = MotherFuckingBullet(copy.copy(self.position), self.angle, self.width, self.height)
        self.bullets.append(bullet)
        
    def crash(self):
        self.crashed = True
        

        