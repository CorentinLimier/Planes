import math, copy
from game.bo.motherFuckingBullet import MotherFuckingBullet

class Plane():
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = [self.width * 0.45, self.height * 0.8]
        self.angle = 0
        self.rotation_speed = 8
        self.speed = 8
        self.crashed = False
        self.bullets = []
        self.hearts = 100
        
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
        self.isCrashed()
        
    def shoot(self):
        position_bullet_x = self.position[0] + 30
        position_bullet_y = self.position[1] + 22
        position_bullet = [position_bullet_x, position_bullet_y]
        bullet = MotherFuckingBullet(position_bullet, self.angle, self.width, self.height)
        self.bullets.append(bullet)
        
    def isCrashed(self):
        if  self.position[0] > self.width or self.position[1] > self.height or self.position[0] < 0 or self.position[1] < 0:
            self.crashed = True
            return True
        if self.hearts < 0 :
            self.crashed = True
            return True
        return False
        