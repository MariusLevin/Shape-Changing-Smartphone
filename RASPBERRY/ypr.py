"""
Created on Mon Jun 11 16:53:56 2018

@author: PECCHIOLI Mathieu
"""

from numpy import array, cos, sin, dot, pi
from math import sqrt, atan

# DEGREES ANGLES
yaw1 = pi/3
pitch1 = pi/4
roll1 = 0

yaw2 = pi/2
pitch2 = 0
roll2 = 0

print("Configuration:")
print(yaw1 * 360 / (2*pi))
print(pitch1 * 360 / (2*pi))
print(roll1 * 360 / (2*pi))
print(yaw2 * 360 / (2*pi))
print(pitch2 * 360 / (2*pi))
print(roll2 * 360 / (2*pi))

# CREATE ROTATION MATRIX
Rz1 = array([[cos(yaw1), -sin(yaw1), 0],
            [sin(yaw1), cos(yaw1), 0],
            [0, 0, 1]])
print(Rz1)
Ry1 = array([[cos(pitch1), 0, sin(pitch1)],
            [0, 1, 0],
            [-sin(pitch1), 0, cos(pitch1)]])
print(Ry1)
Rx1 = array([[1, 0, 0],
            [0, cos(roll1), -sin(roll1)],
            [0, sin(roll1), cos(roll1)]])
print(Rx1)
R1W = dot(Rz1, Ry1, Rx1)
print(R1W)

Rz2 = array([[cos(yaw2), -sin(yaw2), 0],
            [sin(yaw2), cos(yaw2), 0],
            [0, 0, 1]])
print(Rz2)
Ry2 = array([[cos(pitch2), 0, sin(pitch2)],
            [0, 1, 0],
            [-sin(pitch2), 0, cos(pitch2)]])
print(Ry2)
Rx2 = array([[1, 0, 0],
            [0, cos(roll2), -sin(roll2)],
            [0, sin(roll2), cos(roll2)]])
print(Rx2)
R2W = dot(Rz2, Ry2, Rx2)
print(R2W)

# COMBINE MATRICES
R21 = dot(R2W, R1W.T)

# EXTRACT YAW PITCH ROLL BETWEEN SCREEN
yaw21 = atan(R21[1,0] / R21[0,0])
pitch21 = atan(-R21[2,0] / sqrt(R21[2,1] * R21[2,1] + R21[2,2] * R21[2,2]))
roll21 = atan(R21[2,1] / R21[2,2])

print("Solution:")
print(yaw21 * 360 / (2*pi))
print(pitch21 * 360 / (2*pi))
print(roll21 * 360 / (2*pi))