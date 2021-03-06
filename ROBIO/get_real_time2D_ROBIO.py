# -*- coding: cp936 -*-
from math import *
import visual as vs

import random

import numpy as np
import pylab
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import pyplot as plt


def dist( pos1, pos2 ):
    return sqrt( pow(pos1[0]-pos2[0], 2) + pow(pos1[1]-pos2[1], 2) + pow(pos1[2]-pos2[2], 2))

xRange = 121
yRange = 121
zRange = 1

density = [0 for i in range( xRange*yRange*zRange )]

def getDensity(pos):
    if (xRange-1)/2>= pos[0] >= -(xRange-1)/2 and (yRange-1)/2 >= pos[1] >= -(yRange-1)/2 and zRange-1 >= pos[2] >= 0:
        return density[int(((pos[0]+(xRange-1)/2)*yRange+(pos[1]+(yRange-1)/2))*zRange+pos[2])]
    else:
        return -1


# Set the environment here
def drawEnv( sourcePos = (-40, 0, 0), step = 5):
    # Set the environmen(density)
    for i in range(-int((xRange-1)/2), int((xRange-1)/2)):
        for j in range(-int((yRange-1)/2), int((yRange-1)/2)):
            for k in range (0, int(zRange)):
                num = int(((i+(xRange-1)/2)*yRange + (j+(yRange-1)/2))*zRange + k)
                p = (i, j, k)            
                density[num] = 1 / (dist(sourcePos, p)+0.00001)



def makeHoriVector(theta):
    return vs.vector(cos(theta), sin(theta), 0)

def makeVector(theta, phi):
    return vs.vector(cos(theta)*cos(phi), sin(theta)*cos(phi), sin(phi))


def sigmoid(x, alpha = -4):
    return 1.0 / (1.0+exp(-alpha*x)) if x < 10 else 0


maxIter = 1000

maxIterResult = 1000
thre_den = 0.4
time = range(maxIter)
lSensorRec, rSensorRec, distance = range(maxIter),range(maxIter),range(maxIter)

# Implement your strategy for vehicle here
def loopVehicle( sourcePos = (-20, 0, 20), initPos = (40, 40, 0), theta = 3/2*pi, phi = 0, delta = 0.5, alpha = -4, W = 4, maxI = maxIter):
    """ Init & loop vehicle.
    """
    
    initAxis = (cos(theta)*cos(phi), sin(theta)*cos(phi), sin(phi))
    
    vPos, vAxis, vVelocity = vs.vector(initPos), vs.vector(initAxis), vs.vector(initAxis)
    deltat = delta
    vscale = 8

    ii = 0

    while ii < maxIter:
        #vs.rate(3000)

        orthV = makeHoriVector(theta+pi/2)
        orthV2 = makeVector(theta, phi+pi/2)
        lSensorPos = tuple(int(x) for x in (vPos+orthV*W/2).astuple())
        rSensorPos = tuple(int(x) for x in (vPos-orthV*W/2).astuple())
        #print(rSensorPos)

        if (getDensity(lSensorPos) == -1 or getDensity(rSensorPos) == -1) :
            vVelocity = -vVelocity
            vAxis = vVelocity
            vPos = vPos+vVelocity*deltat
            continue
        
        if (getDensity(lSensorPos) > getDensity(rSensorPos)):
            theta = theta + pi/180
        elif getDensity(lSensorPos) < getDensity(rSensorPos):
            theta = theta - pi/180

        vVelocity = makeVector(theta, phi)    
        vPos = vPos+vVelocity*deltat*sigmoid(getDensity(lSensorPos)+getDensity(rSensorPos), alpha)
        vAxis = vVelocity
        
        lSensorRec[ii], rSensorRec[ii], distance[ii] \
                        = getDensity(lSensorPos), getDensity(rSensorPos), dist(sourcePos, vPos.astuple())
        if (lSensorRec[ii] + rSensorRec[ii])/2 > thre_den:
            return ii+1
        ii += 1

stride = 20


step = 1
alphaRate = 0

drawEnv(sourcePos = (-40, 0, 0))
maxIterResult = loopVehicle(theta = 1/2*pi, initPos = (20, 30, 0), sourcePos = (-40, 0, 0), alpha = alphaRate, delta = step)

print lSensorRec[maxIterResult-1], rSensorRec[maxIterResult-1]

time = time[0:maxIterResult:stride]

pylab.figure(1)
plotl, = pylab.plot(time, lSensorRec[0:maxIterResult:stride], '-', label='Left Sensor')
plotr, = pylab.plot(time, rSensorRec[0:maxIterResult:stride], 'o--r', label='Right Sensor')
pylab.legend(loc=2)
pylab.title('Step is '+str(step)+r',$\alpha$ is '+str(alphaRate))
pylab.xlabel('Time')
pylab.ylabel('Density of Sensors')
pylab.grid()
pylab.savefig('./ROBIO/2D_eg_lr_sensor.png', bbox_inches='tight')

newdist = distance[0:maxIterResult:stride]
pylab.figure(2)
plotd,  = pylab.plot(time, newdist, '-b', label='Distanse')
pylab.legend(loc=1)
pylab.title('Step is '+str(step)+r',$\alpha$ is '+str(alphaRate))
pylab.xlabel('Time')
pylab.ylabel('Distance from source')
pylab.grid()
pylab.savefig('./ROBIO/2D_eg_lh_dist.png', bbox_inches='tight')


##step = 1
##alphaRate = -5
##loopVehicle(theta = 1/2*pi, initPos = (20, 20, 0), sourcePos = (-20, 0, 0), alpha = alphaRate, delta = step)
##
##pylab.figure(3)
##plotl, = pylab.plot(time, lSensorRec[::stride], '-', label='Left Sensor')
##plotr, = pylab.plot(time, rSensorRec[::stride], '--r', label='Right Sensor')
##pylab.legend(loc=1)
##pylab.title('Step is '+str(step)+r',$\alpha$ is '+str(alphaRate))
##pylab.xlabel('Time')
##pylab.ylabel('Density of Sensors')
##pylab.grid()
##pylab.savefig('./ROBIO/2D_eg_lr_sensor2.png', bbox_inches='tight')
##
##pylab.figure(4)
##plotd,  = pylab.plot(time, distance[::stride], '-b', label='Distanse')
##pylab.legend(loc=1)
##pylab.title('Step is '+str(step)+r',$\alpha$ is '+str(alphaRate))
##pylab.xlabel('Time')
##pylab.ylabel('Distance from source')
##pylab.grid()
##pylab.savefig('./ROBIO/2D_eg_lh_dist2.png', bbox_inches='tight')


pylab.show()

