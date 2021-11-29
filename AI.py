from tank_class import *
from helper import *

def Go_to_dot(dot,tank):
    fw,fa,fs,fd = 0,0,0,0
    alpha = 0
    if dot.x > tank.center.x:
        alpha = -math.atan((dot.y-tank.center.y) / (dot.x-tank.center.x))
    elif dot.x < tank.center.x:
        alpha = -math.atan((dot.y-tank.center.y) / (dot.x-tank.center.x))+math.pi
    if alpha < 0:
        alpha += 2*math.pi
    beta = convert_ang(tank.body_ang)
    ang = alpha - beta
    if ang <= -math.pi:
        ang += 2*math.pi
    elif ang > math.pi:
        ang -= 2*math.pi
    
    if abs(ang) < math.pi/3:
        fw = 1 
    elif abs(ang) > math.pi/3:
        fs = 1
    if ang > 0:
        fa = 1
    elif ang < 0:
        fd = 1
        
    return fw,fa,fs,fd