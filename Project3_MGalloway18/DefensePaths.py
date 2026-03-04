import math, random
from panda3d.core import *

def CircleX(angle):

    theta = angle

    x = 50 * math.cos(theta)
    y = 50 * math.sin(theta)
    z = 0 * math.tan(theta)

    unitVec = Vec3(x, y, z)
    unitVec.normalize()

    return unitVec

def CircleY(angle):

    theta = angle

    x = 50 * math.cos(theta)
    y = 50 * math.sin(theta)
    z = 0 * math.tan(theta)

    unitVec = Vec3(z, y, x)
    unitVec.normalize()

    return unitVec

def CircleZ(angle):

    theta = angle

    x = 50 * math.cos(theta)
    y = 50 * math.sin(theta)
    z = 0 * math.tan(theta)

    unitVec = Vec3(y, z, x)
    unitVec.normalize()

    return unitVec

def Cloud(radius = 1):
    x = 2 * random.random() - 1
    y = 2 * random.random() - 1
    z = 2 * random.random() - 1

    unitVec = Vec3(x, y, z)
    unitVec.normalize()
    return unitVec * radius

def BaseballSeams(step, numSeams, B, F = 1):
    time = step / float(numSeams) * 2 * math.pi

    F4 = 0

    R = 1

    xxx = math.cos(time) - B * math.cos(3 * time)
    yyy = math.sin(time) + B * math.sin(3 * time)
    zzz = F * math.cos(2 * time) + F4 * math.cos(4 * time)

    rrr = math.sqrt(xxx ** 2 + yyy ** 2 + zzz ** 2)

    x = R * xxx / rrr
    y = R * yyy / rrr
    z = R * zzz / rrr

    return Vec3(x, y, z)