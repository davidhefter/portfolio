### THIS IS USED TO TEST THE REALTIME UPDATE OF MATPLOTLIB PLOTS FOR SIMULATION, NOT USED IN MAIN CODE ###

import matplotlib.pyplot as plt
import numpy as np
import math
import time

z=[1]
x=[0]
y=[0]
t=[0]

thetamax=20 # degrees
zmin = math.cos(thetamax*(math.pi)/180)
xpymax = math.sqrt(1-(zmin*zmin))
step=0.0025
tstart=time.time()
tnow = tstart

plt.ion()
fig = plt.figure(1)
ax = fig.add_subplot(projection='3d')
line1, = plt.plot(x, y, z, label='parametric curve')
line2, = plt.plot([0,0], [0,0], [0,1], label='parametric curve')
fig.canvas.draw()

#x = [0]
#y = [np.sin(x)]
#z = [0]
#
## You probably won't need this if you're embedding things in a tkinter plot...
#plt.ion()
#
#fig = plt.figure(1)
#ax = fig.add_subplot(projection='3d')
#ax.axes.set_xlim3d(left=-3, right=6*np.pi) 
#ax.axes.set_ylim3d(bottom=-3, top=6*np.pi) 
#ax.axes.set_zlim3d(bottom=-1, top=1) 
#line1, = ax.plot(x, y, z, label='parametric curve') # Returns a tuple of line objects, thus the comma
#line2, = ax.plot(y, x, z, label='parametric curve')
#
#for phase in np.linspace(0, 6*np.pi, 500):
#    x.append(phase)
#    y.append(np.sin(x[-1]))
#    z.append(0)
#    line1.set_data_3d(x, y, z)
#    line2.set_data_3d(y, x, z)
#    fig.canvas.draw()
#    fig.canvas.flush_events()