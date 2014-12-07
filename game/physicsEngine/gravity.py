
from game.bo.position import Position
import math

def computeGravity(position, speed, angle, elapsed_time, gravity_coeff=9.82):
    
    new_position = Position()
    new_position.x = position.x + speed * elapsed_time * math.cos(angle)
    new_position.y = position.y -0.5 * gravity_coeff * math.pow(elapsed_time, 2) + elapsed_time * speed * math.sin(angle)
    return new_position
    