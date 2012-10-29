from __future__ import division
from pylab import *
import math
import matplotlib.pyplot as plt

def func3(x,y):
    omega=0.04*x + 0.05
    x_ = [[math.sqrt(i) for i in j] for j in x]
    return 1 - exp(-(y-x_)**2 / (2*omega**2))
def func2(x,y):
    omega=0.04*x + 0.05
    x_ = [[math.sqrt(i) for i in j] for j in x]
    return 1 - exp(-(2.5-y-x_)**2 / (2*omega**2))
def func1(x,y):
    omega=0.08
    return 1 - exp(-(y-2)**2 / (2*omega**2))


# make these smaller to increase the resolution
dx, dy = 0.05, 0.05

x = arange(0.0, 3.0001, dx)
y = arange(0.0, 3.0001, dy)
X,Y = meshgrid(x, y)

Z = func3(X, Y)
pcolor(X, Y, Z, cmap=plt.bone(), alpha=1.0)

Z = func2(X, Y)
pcolor(X, Y, Z, cmap=plt.bone(), alpha=0.5)

Z = func1(X, Y)
pcolor(X, Y, Z, cmap=plt.bone(), alpha=0.3)


axis([0,3,0,3])
show()