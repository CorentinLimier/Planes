'''
Created on 21 déc. 2014

@author: cocoloco
'''

import math

class MovingObject():
    
    def __init__(self, width, height, position, angle, speed, rotation_speed):
        self.width = width
        self.height = height
        self.position = position
        self.angle = angle
        self.speed = speed
        self.rotation_speed = rotation_speed
        self.crash = False
        
    def turn_left(self, frame_count=1):
        self.angle += self.rotation_speed
    
    def turn_right(self, frame_count=1):
        self.angle -= self.rotation_speed
        
    def move_forward(self, frame_count = 1):
        angle = math.radians(self.angle)
        self.position[0] += self.speed * frame_count * math.cos(angle)
        self.position[1] -= self.speed * frame_count * math.sin(angle)
        self.update_crashed()
    
    def update_crashed(self):
        if  self.position[0] > self.width or self.position[1] > self.height or self.position[0] < 0 or self.position[1] < 0:
            self.crashed = True
        if self.hearts < 0 :
            self.crashed = True 
        