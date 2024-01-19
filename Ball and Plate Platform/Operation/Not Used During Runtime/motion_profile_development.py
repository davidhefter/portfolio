import math
import time


### THIS CODE IS NOT USED IN RUNNING THE MAIN SYSTEM, ONLY FOR PRE-MAKING MOTION PROFILES ###


# plug in initial time, max inclination from vertical, and run speed
# the program will move in a circle at max inclination from vertical,
# in which the speed of the rotation around is determined by run speed
def circle(t0, theta_max, speed, time_factor):
    del_t = (time.monotonic_ns()-t0)/time_factor                                 # time elapsed
    
    # align platform to circle starting position
    if del_t < theta_max/speed:
        theta_cur = speed*del_t                                                 # rotation down to inclination angle
        x = -math.sin(math.radians(theta_cur))*math.cos(math.radians(0))        # find x (phi=0 required for rotation about correct axis)
        y = -math.sin(math.radians(theta_cur))*math.sin(math.radians(0))        # find y (phi=0 required for rotation about correct axis)
        z = -math.cos(math.radians(theta_cur))                                  # find z
    # after platform is aligned, make circle
    else:
        del_t = del_t - (theta_max/speed)                                       # offset time after alignment   
        phi_cur = (speed*del_t)%360                                             # rotation about circle, capped at 360deg
        x = -math.sin(math.radians(theta_max))*math.cos(math.radians(phi_cur))  # find x
        y = -math.sin(math.radians(theta_max))*math.sin(math.radians(phi_cur))  # find y
        z = -math.cos(math.radians(theta_max))                                  # find z
    #return [x,y,z]
    return [i * (180/math.pi) for i in xyz_to_th1th2(x,y,z)]                    # convert xyz to th1th2 in degrees

# plug in initial time, max inclination from vertical, and run speed
# the program will move about the x-axis in both directions, with max inclination 
# of theta_max, and rate of change of inclination determined by run speed
def th3sweep(t0, theta_max, speed, time_factor):
    del_t = (time.monotonic_ns()-t0)/time_factor                         # time elapsed

    # generate motion pattern capped at positive and negative ends by theta_max /\/\/\/\/\/\/\/
    if int(((speed*del_t)/theta_max)%4) == 0:
        theta_cur = (speed*del_t)%theta_max
    elif int(((speed*del_t)/theta_max)%4) == 1:
        theta_cur = theta_max - ((speed*del_t)%theta_max)
    elif int(((speed*del_t)/theta_max)%4) == 2:
        theta_cur = -((speed*del_t)%theta_max)
    else:
        theta_cur = -theta_max + ((speed*del_t)%theta_max)


    x = -math.sin(math.radians(theta_cur))*math.cos(math.radians(-90))  # find x (phi=-90 required for rotation about correct axis)
    y = -math.sin(math.radians(theta_cur))*math.sin(math.radians(-90))  # find y (phi=-90 required for rotation about correct axis)
    z = -math.cos(math.radians(theta_cur))                              # find z
    
    return [i * (180/math.pi) for i in xyz_to_th1th2(x,y,z)]            # convert xyz to th1th2 in degrees

# plug in initial time, max inclination from vertical, and run speed
# the program will move about the y-axis in both directions, with max inclination 
# of theta_max, and rate of change of inclination determined by run speed
def th4sweep(t0, theta_max, speed, time_factor):
    del_t = (time.monotonic_ns()-t0)/time_factor                         # time elapsed
    
    # generate motion pattern capped at positive and negative ends by theta_max /\/\/\/\/\/\/\/
    if int(((speed*del_t)/theta_max)%4) == 0:
        theta_cur = (speed*del_t)%theta_max
    elif int(((speed*del_t)/theta_max)%4) == 1:
        theta_cur = theta_max - ((speed*del_t)%theta_max)
    elif int(((speed*del_t)/theta_max)%4) == 2:
        theta_cur = -((speed*del_t)%theta_max)
    else:
        theta_cur = -theta_max + ((speed*del_t)%theta_max)

    x = -math.sin(math.radians(theta_cur))*math.cos(math.radians(0))    # find x (phi=0 required for rotation about correct axis)
    y = -math.sin(math.radians(theta_cur))*math.sin(math.radians(0))    # find y (phi=0 required for rotation about correct axis)
    z = -math.cos(math.radians(theta_cur))                              # find z

    return [i * (180/math.pi) for i in xyz_to_th1th2(x,y,z)]            # convert xyz to th1th2 in degrees

def xyz_to_th1th2(x, y, z):
    th3 = math.atan(-y/z)                                               # th3 in radians
    if x!=0:
        th4 = -(abs(x)/x)*math.atan( math.sqrt((x*x) / ((y*y)+(z*z))) ) # th4 in radians
    else:
        th4 = 0                                                         # th4 in radians when x=0 (to prevent 0/0 issues)
    th1 = th3+th4                                                       # find th1
    th2=th3-th4                                                         # find th2
    return [th1, th2]

if __name__ == "__main__":
    t0 = time.monotonic_ns()    # start time
    theta_max = 20              # maximum inclination from vertical, in degrees
    speed = 20                  # degree per second, use varies by function see function description
    gear_ratio=3                # self explanatory
    run_time = 5                # runtime in seconds
    t_delay = t0                # time pointer for delay function
    delay_step = 0.01           # approximate timestep for delay, won't be totally perfect
    time_factor = 1000000000    # conversion from time reading to seconds (currently in nanoseconds)

    # initial print of motor positions
    [th1, th2] = circle(t0, theta_max, speed, time_factor)
    print((time.monotonic_ns()-t0)/time_factor, [gear_ratio*th1, gear_ratio*th2])

    # while time elapsed is less than run time
    while ((time.monotonic_ns()-t0)/time_factor)<run_time:
        # if time elapsed since last time pointer is more than the delay length
        if ((time.monotonic_ns()-t_delay)/time_factor)>delay_step:
            # adjust delay length
            t_delay = time.monotonic_ns()

            # use motion function to find th1 and th2 in degrees and print
            [th1, th2] = circle(t0, theta_max, speed, time_factor)
            print((time.monotonic_ns()-t0)/time_factor, [gear_ratio*th1, gear_ratio*th2])
            
    # final print of motor positions     
    [th1, th2] = circle(t0, theta_max, speed, time_factor)
    print((time.monotonic_ns()-t0)/time_factor,[gear_ratio*th1, gear_ratio*th2])