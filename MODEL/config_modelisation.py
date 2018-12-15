from math import sin, cos, radians, degrees
import numpy as np
import os

# os.system('clear')

length = 7.5
width = 5.5
height = 2

print("START PROGRAM")

alpha = input("Enter your alpha angle please: ")
beta = input("Enter your beta angle please: ")

alpha = radians((ord(alpha[0]) - ord('0')) * 10 + (ord(alpha[1]) - ord('0')))
beta = radians(-1 * ((ord(beta[0]) - ord('0')) * 10 + (ord(beta[1]) - ord('0'))))

Rx = np.array([[1, 0, 0], [0, cos(alpha), -sin(alpha)], [0, sin(alpha), cos(alpha)]])
# Ry = np.array([[cos(beta), 0, sin(beta)], [0, 1, 0], [-sin(beta), 0, cos(beta)]])
Rz = np.array([[cos(beta), -sin(beta), 0], [sin(beta), cos(beta), 0], [0, 0, 1]])

Mtransfert = np.dot(Rx, Rz)

X1 = np.array([[0],[0],[0]])
X2 = np.array([[0],[0],[-height]])
X3 = np.array([[0],[length],[0]])
X4 = np.array([[0],[length],[-height]])
X5 = np.array([[-width],[0],[0]])
X6 = np.array([[-width],[0],[-height]])
X7 = np.array([[-width],[length],[0]])
X8 = np.array([[-width],[length],[-height]])

X1new = np.dot(Mtransfert, X1)
X2new = np.dot(Mtransfert, X2)
X3new = np.dot(Mtransfert, X3)
X4new = np.dot(Mtransfert, X4)
X5new = np.dot(Mtransfert, X5)
X6new = np.dot(Mtransfert, X6)
X7new = np.dot(Mtransfert, X7)
X8new = np.dot(Mtransfert, X8)

print("X1" + str(X1new))
print("X2" + str(X2new))
print("X3" + str(X3new))
print("X4" + str(X4new))
print("X5" + str(X5new))
print("X6" + str(X6new))
print("X7" + str(X7new))
print("X8" + str(X8new))
