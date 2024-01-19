### THIS CODE IS USED FOR SIMULATING THE MOTION OF THE PLATFORM USING A MOTION PROFILE, NOT USED IN THE MAIN CODE ###
import numpy as np
import matplotlib.pyplot as plt
import math
import keyboard 
import time

cond = True
i=1
z=[1]
x=[0]
y=[0]
t=[0]

thetamax=20 # degrees
zmin = math.cos(thetamax*(math.pi)/180)
xpymax = math.sqrt(1-(zmin*zmin))
step=0.0085
tstart=time.time()
tnow = tstart

plt.ion()
fig = plt.figure(1)
ax = fig.add_subplot(projection='3d')
line1, = plt.plot(x, y, z, label='parametric curve')
line2, = plt.plot([0,0], [0,0], [0,1], label='parametric curve')
fig.canvas.draw()
fig.canvas.flush_events()
ax.axes.set_xlim3d(left=-1, right=1) 
ax.axes.set_ylim3d(bottom=-1, top=1) 
ax.axes.set_zlim3d(bottom=0, top=1)
plt.gca().set_aspect('equal')


while cond:
    if time.time()-tnow>=0.001:
        updated = False
        if keyboard.is_pressed('g'):
            t.append(time.time()-tstart)
            tnow=time.time()
            x.append(x[i-1])
            y.append(y[i-1]+step)
            z.append(math.sqrt(1-(x[i]*x[i])-(y[i]*y[i])))
            if z[i]<=zmin:
                z[i]=zmin
                if abs(y[i])>=xpymax:
                    if y[i]>=0:
                        y[i]=xpymax
                    else:
                        y[i]=-xpymax
                if x[i]>=0:
                    x[i]=math.sqrt(1-(z[i]*z[i])-(y[i]*y[i]))
                else:
                    x[i]=-math.sqrt(1-(z[i]*z[i])-(y[i]*y[i]))
            i+=1
        if keyboard.is_pressed('v'):
            t.append(time.time()-tstart)
            tnow=time.time()
            x.append(x[i-1]-step)
            y.append(y[i-1])
            z.append(math.sqrt(1-(x[i]*x[i])-(y[i]*y[i])))
            if z[i]<=zmin:
                z[i]=zmin
                if abs(x[i])>=xpymax:
                    if x[i]>=0:
                        x[i]=xpymax
                    else:
                        x[i]=-xpymax
                if y[i]>=0:
                    y[i]=math.sqrt(1-(z[i]*z[i])-(x[i]*x[i]))
                else:
                    y[i]=-math.sqrt(1-(z[i]*z[i])-(x[i]*x[i]))
            i+=1
        if keyboard.is_pressed('b'):
            t.append(time.time()-tstart)
            tnow=time.time()
            x.append(x[i-1])
            y.append(y[i-1]-step)
            z.append(math.sqrt(1-(x[i]*x[i])-(y[i]*y[i])))
            if z[i]<=zmin:
                z[i]=zmin
                if abs(y[i])>=xpymax:
                    if y[i]>=0:
                        y[i]=xpymax
                    else:
                        y[i]=-xpymax
                if x[i]>=0:
                    x[i]=math.sqrt(1-(z[i]*z[i])-(y[i]*y[i]))
                else:
                    x[i]=-math.sqrt(1-(z[i]*z[i])-(y[i]*y[i]))
            i+=1
        if keyboard.is_pressed('n'):
            t.append(time.time()-tstart)
            tnow=time.time()
            x.append(x[i-1]+step)
            y.append(y[i-1])
            z.append(math.sqrt(1-(x[i]*x[i])-(y[i]*y[i])))
            if z[i]<=zmin:
                z[i]=zmin
                if abs(x[i])>=xpymax:
                    if x[i]>=0:
                        x[i]=xpymax
                    else:
                        x[i]=-xpymax
                if y[i]>=0:
                    y[i]=math.sqrt(1-(z[i]*z[i])-(x[i]*x[i]))
                else:
                    y[i]=-math.sqrt(1-(z[i]*z[i])-(x[i]*x[i]))
            i+=1
        if keyboard.is_pressed('\n'):
            cond=False
        else:
            line1.set_data_3d(x, y, z)
            line2.set_data_3d([0,x[-1]], [0,y[-1]], [0,z[-1]])
            fig.canvas.draw()
            fig.canvas.flush_events()
    
#plt.figure(2).add_subplot(projection='3d')
#plt.plot(x, y, z, label='parametric curve')       # Plot the sine of each x point
#plt.plot([0,0], [0,0], [0,1], label='parametric curve')       # Plot the sine of each x point
#plt.grid()
#plt.gca().set_aspect('equal')
#plt.axhline(linewidth=1, color="k")
#plt.axvline(linewidth=1, color="k")

#plt.show()                   # Display the plot


#size=100
#t = np.linspace(0, 6*math.pi, size)  # Create a list of evenly-spaced numbers over the range
#x = (2.5*np.cos(t)+5*np.cos(2*t/3))/22
#y = (2.5*np.sin(t)-5*np.sin(2*t/3))/22
#z = size*[0]
#for i in range(size):
#    z[i]=math.sqrt(1-(x[i]*x[i])-(y[i]*y[i]))
#plt.figure(1).add_subplot(projection='3d')
#plt.plot(x, y, z, label='parametric curve')       # Plot the sine of each x point
#plt.plot([0,0], [0,0], [0,1], label='parametric curve')       # Plot the sine of each x point
#plt.grid()
#plt.gca().set_aspect('equal')
#plt.axhline(linewidth=1, color="k")
#plt.axvline(linewidth=1, color="k")

#plt.show()                   # Display the plot
#at = np.linspace(0, 6*math.pi, size)