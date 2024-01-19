"""! 
@file main.py
    This file contains the main
    
    @author David Hefter, Mathew Smith, Akanksha Maddi, Amanda Westmoreland
    @date   31-Oct-2023
    @copyright (c) 2023 by Nobody and released under GNU Public License v3
"""
import math
import utime
import gc
import pyb
from pyb import Pin, Timer, ADC, UART, SPI
import cotask
import task_share
from machine import I2C
from pi_control import PI_Control
from motor_driver import Motor_Driver
from encoder_reader import Encoder_Reader

m_one_controller = 0
m_two_controller = 0
backlash_test_state = 0

def motor_one(shares):
    """!
    This function contains the task for controlling the left motor. 

    @param shares: A list holding the shared variables used by this task
    """
    ## M12TIM
    tim3 = Timer(3, freq = 20000)

    # Create motor one
    ## M1PWM pin (PWM)
    PC6 = Pin(Pin.cpu.C6, mode=Pin.ALT, af=2)
    ## M1DIR pin (direction)
    PC7 = Pin(Pin.cpu.C7, mode=Pin.OUT_PP)
    ## M1!SLP pin (set high to unsleep driver)
    PC13 = Pin(Pin.cpu.C13, mode=Pin.OUT_OD)
    ## M1!FLT pin (goes low when there's a fault)
    PC2 = Pin(Pin.cpu.C2)#, mode=Pin.IN, pull=Pin.PULL_UP)
    ## M1CS pin (current sensor)
    PC0 = Pin(Pin.cpu.C0, mode=Pin.ANALOG)
    ## M1CS ADC (current sensor)
    M1CS = ADC(PC0)
    ## M1PWM timer channel
    ch3_1 = tim3.channel(1, mode=Timer.PWM)
    # create motor
    m = Motor_Driver(tim3, PC6, PC7, PC13, PC2, PC0, M1CS, ch3_1)
    m.enable()

    ## Create encoder one
    ## E1TIM
    tim4 = Timer(4, period=0xFFFF, prescaler=0, mode=Timer.UP)
    ## E1CHA pin
    PB6 = Pin(Pin.cpu.B6, mode=Pin.ALT, af=2)
    ## E1CHB pin
    PB7 = Pin(Pin.cpu.B7, mode=Pin.ALT, af=2)
    ## E1 interrupt timer
    #tim6 = Timer(6, freq=512, callback=E1CB)
    tim6_chan = 6
    tim6_freq = 512
    # create encoder
    e = Encoder_Reader(tim4, PB6, PB7, tim6_chan, tim6_freq)

    # Set up control class
    Kp = 0.065      # Motor control parameter
    Ki = 0.00065
    Kd = 0.00085
    c = PI_Control(Kp, Ki, Kd, 0, e, m)
    
    global m_one_controller 
    m_one_controller = c
    # Get references to the share and queue which have been passed to this task
    yield 0
    while True:
        c.run(m1_target.get())
        m.set_duty_cycle(c.pwm)
        m1_position.put(e.read())
        #c.get_pwm()
        yield 0


def motor_two(shares):
    """!
    This function contains the task for controlling the right motor. 

    @param shares: A list holding the shared variables used by this task
    """
    ## M12TIM
    tim3 = Timer(3, freq = 20000)
    
    # create motor two
    ## M2PWM pin
    PB0 = Pin(Pin.cpu.B0, mode=Pin.ALT, af=2)
    ## M2DIR pin
    PB1 = Pin(Pin.cpu.B1, mode=Pin.OUT_PP)
    ## M2!SLP pin
    PB4 = Pin(Pin.cpu.B4, mode=Pin.OUT_OD)
    ## M2!FLT pin
    PB5 = Pin(Pin.cpu.B5, mode=Pin.IN, pull=Pin.PULL_UP)
    ## M2CS pin
    PC1 = Pin(Pin.cpu.C1, mode=Pin.ANALOG)
    ## M2CS ADC
    M2CS = ADC(PC1)
    ## M2PWM timer channel
    ch3_3 = tim3.channel(3, mode=Timer.PWM)
    # create motor
    m = Motor_Driver(tim3, PB0, PB1, PB4, PB5, PC1, M2CS, ch3_3)
    m.enable()

    # create encoder two
    ## E2TIM
    tim5 = Timer(5, period=0xFFFF, prescaler=0, mode=Timer.UP)
    ## E2CHA pin
    PA0 = Pin(Pin.cpu.A0, mode=Pin.ALT, af=2)
    ## E2CHB pin
    PA1 = Pin(Pin.cpu.A1, mode=Pin.ALT, af=2)
    ## E2 interrupt timer
    #tim7 = Timer(7, freq=512, callback=E2CB)
    tim7_chan = 7
    tim7_freq = 512
    # create encoder
    e = Encoder_Reader(tim5, PA0, PA1, tim7_chan, tim7_freq)

    # Set up control class
    Kp = 0.065      # Motor control parameter
    Ki = 0.00065
    Kd = 0.00085  
    c = PI_Control(Kp, Ki, Kd, 0, e, m)
    
    global m_two_controller
    m_two_controller = c
    # Get references to the share and queue which have been passed to this task
    yield 0
    while True:
        c.run(m2_target.get())
        m.set_duty_cycle(c.pwm)
        m2_position.put(e.read())
        #c.get_pwm()
        yield 0

def position(shares):
    """!
    This function contains the task for controlling the motor targets based on the motion profiles. 

    @param shares: A list holding the shared variables used by this task
    """

    m1_position, m2_position, m1_target, m2_target = shares
    t0 = utime.ticks_ms()    # start time
    theta_max = 4              # maximum inclination from vertical, in degrees
    speed = 80                   # degrees per second, use varies by function see function description
    gear_ratio=3                # self explanatory
    t_delay = t0                # time pointer for delay function
    delay_step = 0.0001         # approximate timestep for delay, won't be totally perfect
    time_factor = 1000          # conversion from time reading to seconds (currently in milliseconds)
    tick_factor = 4096/360      # tick/deg
    run_time = 6000             # ms, only for babytest
    
    while True:
        # if time elapsed since last time pointer is more than the delay length
        if ((utime.ticks_ms()-t_delay)/time_factor)>delay_step:
            # adjust delay length
            t_delay = utime.ticks_ms()

            # use motion profile to find th1 and th2 in degrees and print
            #[th1, th2] = basic_motor_test(t0, speed, run_time, gear_ratio, tick_factor, time_factor) # don't run when attached
            #[th1, th2] = backlash_test(t0, time_factor)
            [th1, th2] = circle(t0, theta_max, speed, time_factor)
            #[th1, th2] = keyboardcontrol(theta_max, speed, m1_target.get()/tick_factor, -1*m2_target.get()/tick_factor)
            #print(th1 * gear_ratio * tick_factor, th2 * gear_ratio * tick_factor)
            #[th1, th2] = th3sweep(t0, theta_max, speed, time_factor)
            m1_target.put(th1 * gear_ratio * tick_factor)
            m2_target.put(th2 * gear_ratio * tick_factor * -1)
            print(str([m1_target.get(), m1_position.get()]) + " | " + str([m2_target.get(), m2_position.get()]))
            yield 0

def keyboardcontrol(theta_max, speed, th1_old, th2_old):
    """!
    This function contains a motion profile in which the user can control the platform with keyboard inputs. 

    @param theta_max: The maximum angle from vertical the platform is allowed to go
    @param speed: The variable controlling how far each motion step moves
    @param th1_old: The previous th1
    @param th2_old: The previous th2
    """
    th1_old = th1_old*math.pi/180
    th2_old = th2_old*math.pi/180
    a = th1_old
    b = th2_old
    zmin = math.cos(theta_max*(math.pi)/180)
    xpymax = math.sqrt(1-(zmin*zmin))
    step=speed/100000
    [x_old,y_old,z_old]=th1th2_to_xyz(th1_old, th2_old)
    x1 = x_old
    y1 = y_old
    z1 = z_old
    ser = pyb.USB_VCP()
    if ser.any():
        charIn = ser.read(1).decode()

        if charIn == 'w':
            x = x_old
            y = y_old+step
            z = -(math.sqrt(1-(x*x)-(y*y)))
            if abs(z)<=zmin:
                z=-zmin
                if abs(y)>=xpymax:
                    if y>=0:
                        y=xpymax
                    else:
                        y=-xpymax
                if x>=0:
                    x=math.sqrt(1-(z*z)-(y*y))
                else:
                    x=-math.sqrt(1-(z*z)-(y*y))
            x_old=x
            y_old=y
            z_old=z

        if charIn == 'a':
            x = x_old-step
            y = y_old
            z = -(math.sqrt(1-(x*x)-(y*y)))
            if abs(z)<=zmin:
                z=-zmin
                if abs(x)>=xpymax:
                    if x>=0:
                        x=xpymax
                    else:
                        x=-xpymax
                if y>=0:
                    y=math.sqrt(1-(z*z)-(x*x))
                else:
                    y=-math.sqrt(1-(z*z)-(x*x))
            x_old=x
            y_old=y
            z_old=z

        if charIn == 's':
            x = x_old
            y = y_old-step
            z = -(math.sqrt(1-(x*x)-(y*y)))
            if abs(z)<=zmin:
                z=-zmin
                if abs(y)>=xpymax:
                    if y>=0:
                        y=xpymax
                    else:
                        y=-xpymax
                if x>=0:
                    x=math.sqrt(1-(z*z)-(y*y))
                else:
                    x=-math.sqrt(1-(z*z)-(y*y))
            x_old=x
            y_old=y
            z_old=z

        if charIn == 'd':
            x = x_old+step
            y = y_old
            z = -(math.sqrt(1-(x*x)-(y*y)))
            if abs(z)<=zmin:
                z=-zmin
                if abs(x)>=xpymax:
                    if x>=0:
                        x=xpymax
                    else:
                        x=-xpymax
                if y>=0:
                    y=math.sqrt(1-(z*z)-(x*x))
                else:
                    y=-math.sqrt(1-(z*z)-(x*x))
            x_old=x
            y_old=y
            z_old=z
    x2 = x_old
    y2 = y_old
    z2 = z_old
    #print(str([x1, x2])+" | "+str([y1, y2])+" | "+str([z1, z2]))
    #print([i * (180/math.pi) for i in xyz_to_th1th2(x_old,y_old,z_old)])
    return [i * (180/math.pi) for i in xyz_to_th1th2(x_old,y_old,z_old)]        

def basic_motor_test(t0, speed, run_time, gear_ratio, tick_factor, time_factor):
    # speed in degrees per second
    del_t = (utime.ticks_ms()-t0)/time_factor    # seconds
    if del_t > (run_time/time_factor):
        end_pos = speed*(run_time/time_factor)   # degrees
        return [end_pos, end_pos]            # don't change position
    else:
        # true speed (degrees per second) is speed(ticks per second)/tick_factor(ticks per degree)
        target = speed*del_t # degrees
        return [target, target] # ticks / (ticks/degree)

def backlash_test(time_factor):
    speed = 35
    theta_max = 10
    ser = pyb.USB_VCP()
    if backlash_test_state==0:
        print("Waiting to start")
        if ser.any():
            charIn = ser.read(1).decode()
            if charIn == ' ':
                backlash_test_state = 1
                t0 = utime.ticks_ms()
        return [0,0] 
    elif backlash_test_state==1:
        print("Going first way")
        if ser.any():
            charIn = ser.read(1).decode()
            if charIn == ' ':
                backlash_test_state = 0
        del_t = (utime.ticks_ms()-t0)/time_factor                                 # time elapsed
        # attempt to move gear forward 5 degrees
        if del_t < theta_max/speed:
            theta = speed*del_t                                                 # rotation down to inclination angle
        # after incrementing to stopping position, hold position
        else:
            backlash_test_state=2
            theta = theta_max
            t0=utime.ticks_ms()
        #return [x,y,z]
        return [theta,0]                    # convert xyz to th1th2 in degrees   
    elif backlash_test_state==2:
        print("Going second way")
        if ser.any():
            charIn = ser.read(1).decode()
            if charIn == ' ':
                backlash_test_state = 0
        del_t = (utime.ticks_ms()-t0)/time_factor                                 # time elapsed
        # attempt to move gear forward 5 degrees
        if del_t < 2*(theta_max/speed):
            theta = theta_max-speed*del_t                                                 # rotation down to inclination angle
        # after incrementing to stopping position, hold position
        else:
            theta = -theta_max
        #return [x,y,z]
        return [theta,0]                    # convert xyz to th1th2 in degrees

def circle(t0, theta_max, speed, time_factor):
    """!
    This function contains a motion profile in which the platform moves in a circular/conical path around the vertical axis. 

    @param t0: The time that the function was called
    @param theta_max: The maximum angle from vertical the platform is allowed to go
    @param speed: The variable controlling the angular speed around the vertical axis
    @param time_factor: The conversion between tick time units and seconds
    """
    del_t = (utime.ticks_ms()-t0)/time_factor                                 # time elapsed
    
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
    """!
    This function contains a motion profile in which the platform sweeps back and forth along the th3 axis. 

    @param t0: The time that the function was called
    @param theta_max: The maximum angle from vertical the platform is allowed to go
    @param speed: The variable controlling the speed around the th3 axis
    @param time_factor: The conversion between tick time units and seconds
    """
    del_t = (utime.ticks_ms()-t0)/time_factor                         # time elapsed

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
    """!
    This function contains a motion profile in which the platform sweeps back and forth along the th4 axis. 

    @param t0: The time that the function was called
    @param theta_max: The maximum angle from vertical the platform is allowed to go
    @param speed: The variable controlling the speed around the th4 axis
    @param time_factor: The conversion between tick time units and seconds
    """
    del_t = (utime.ticks_ms()-t0)/time_factor                         # time elapsed
    
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

def th1th2_to_xyz(th1, th2):
    """!
    This function transforms the th1 th2 coordinate system into XYZ coordinate system. 

    @param th1: Angular position of gear 1
    @param th2: Angular position of gear 2
    """
    th3 = (th1+th2)/2
    th4 = (th1-th2)/2
    x = -math.cos(th3)*math.sin(th4)
    y = math.sin(th3)
    z = -math.cos(th3)*math.cos(th4)
    return[x,y,z]

def xyz_to_th1th2(x, y, z):
    """!
    This function transforms the XYZ coordinate system into th1 th2 coordinate system. 

    @param x: Length of unit vector along horizontal axis 1
    @param y: Length of unit vector along horizontal axis 2
    @param z: Length of unit vector along vertical axis
    """
    th3 = math.atan(-y/z)                                               # th3 in radians
    if x!=0:
        th4 = -(abs(x)/x)*math.atan( math.sqrt((x*x) / ((y*y)+(z*z))) ) # th4 in radians
    else:
        th4 = 0                                                         # th4 in radians when x=0 (to prevent 0/0 issues)
    th1 = th3+th4                                                       # find th1
    th2=th3-th4                                                         # find th2
    return [th1, th2]

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    m1_position = task_share.Share('h', thread_protect = False, name = "m1_position")
    m2_position = task_share.Share('h', thread_protect = False, name = "m2_position")
    m1_target = task_share.Share('f', thread_protect = False, name = "m1_target")
    m2_target = task_share.Share('f', thread_protect = False, name = "m2_target")
    
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(motor_one, name="motor_one", priority=1, period=10,
                        profile=True, trace=False, shares=(m1_position, m2_position, m1_target, m2_target))
    task2 = cotask.Task(motor_two, name="motor_two", priority=1, period=10,
                        profile=True, trace=False, shares=(m1_position, m2_position, m1_target, m2_target))
    task3 = cotask.Task(position, name="position", priority=0, period=1,
                        profile=True, trace=False, shares=(m1_position, m2_position, m1_target, m2_target))
    
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)


    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            time = utime.ticks_ms()
            while utime.ticks_ms() - time <= 350:
                m_one_controller.run(0)
                m_two_controller.run(0)
            m_one_controller.motor.set_duty_cycle(0)
            m_two_controller.motor.set_duty_cycle(0)
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')
