import math
import traceback
from game.bo.motherFuckingBullet import MotherFuckingBullet


class Plane():
    
    def __init__(self, width=None, height=None, position=None):
        self.width = width
        self.height = height
        self.position = position
        self.angle = 0
        self.rotation_speed = 5
        self.speed = 5
        self.crashed = False
        self.bullets = []
        self.hearts = 100
        
    def turn_left(self, frame_count=1):
        self.angle += self.rotation_speed
    
    def turn_right(self, frame_count=1):
        self.angle -= self.rotation_speed
        
    def update(self):
        crashed_bullets = []
        for bullet in self.bullets:
            if bullet.crashed:
                crashed_bullets.append(bullet)
            else:
                bullet.update()
        for bullet in crashed_bullets:
            self.bullets.remove(bullet)
        self.move_forward()
        
    def move_forward(self, frame_count=1):
        angle = math.radians(self.angle)
        # debug only
        # if self.position is None:
        #    traceback.print_exc()
        # print self.position, self.speed, frame_count, angle
        self.position[0] += self.speed * frame_count * math.cos(angle)
        self.position[0] %= self.width
        self.position[1] -= self.speed * frame_count * math.sin(angle)
        self.is_crashed()
        if self.position > (self.width, self.height) or self.position > (self.width, self.height):
            self.crash()
        
    def shoot(self):
        position_bullet_x = self.position[0] + 30
        position_bullet_y = self.position[1] + 22
        position_bullet = [position_bullet_x, position_bullet_y]
        bullet = MotherFuckingBullet(position_bullet, self.angle, self.width, self.height)
        self.bullets.append(bullet)

    def crash(self):
        self.crashed = True

    def is_crashed(self):
        if self.position[0] > self.width or self.position[1] > self.height or self.position[0] < 0 or self.position[1] < 0:
            self.crashed = True
            return True
        if self.hearts < 0:
            self.crashed = True
            return True
        return False