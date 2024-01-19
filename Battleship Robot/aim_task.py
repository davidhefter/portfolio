'''!    @file aim_task.py
        @brief                                  controls stepper motors to aim ping poing ball cannon
                                                
        @author                                 Hefter, David
        @author                                 OConnell, Joseph
                                                
        @date                                   November 28, 2022
'''

import stepper_driver,time
from pyb import Pin, Timer

def AimTaskFcn( columnNum, rowNum, FireSignal, LoadSignal, shoot ):
    
    state = 0
    
    # possible angles
    # need to find this via testing
    theta_0 = 45*5
    theta_1 = 35*5
    theta_2 = 25*5
    theta_3 = 15*5
    theta = [theta_0, theta_1, theta_2, theta_3]
    
    # possible x positions
    # need to find these via testing
    x_0 = 0
    x_1 = 300
    x_2 = 600
    x_3 = 900
    x = [x_0, x_1, x_2, x_3]
    
    hold = False
    
    while True:
        
        # STATE 0: INIT
        if state == 0:
            # make stepper objects
            timer = Timer(8, freq = 20000000)
            CLKpin = Pin.cpu.C7
            SPInum = 2            
            CSpin1 = Pin.cpu.C3
            CSmode1 = Pin.OUT_PP
            CSvalue1 = 1
            ENpin1 = Pin.cpu.B6            
            CSpin2 = Pin.cpu.C2
            CSmode2 = Pin.OUT_PP
            CSvalue2 = 1
            ENpin2 = Pin.cpu.C0
            
            motors = stepper_driver.Stepper_Driver(2, timer, CLKpin, SPInum, CSpin1, CSmode1, CSvalue1, CSpin2, CSmode2, CSvalue2, ENpin1, ENpin2)
            
            state = 1
            motors.set_position(1,0)
            motors.set_position(2,0)
        
        # STATE 1: WAIT_TO_ROLL
        elif state == 1:
            # wait for user call
            
            if shoot.get():
                angle = theta[rowNum.get()]
                position = x[columnNum.get()]
                shoot.put(False)
                state = 2
                hold = False
        
        # STATE 2: ROLL        
        elif state == 2:
            # take wheel to appropriate positions
            # set LoadSignal
            motors.set_position(2,position)
            if (abs(int(motors.get_position(2)) -  position) <= 1):
                if not hold:
                    start_time = time.ticks_ms()
                    hold = True
                if time.ticks_ms()>start_time+1000:
                    LoadSignal.put(True)
                    state = 3
        # STATE 3: WAIT_TO_TILT
        elif state == 3:
            if not LoadSignal.get():
                motors.set_position(1,angle)
                state = 4
        # STATE 4: TILT
        elif state == 4:
            if (abs(int(motors.get_position(1)) -  angle) <= 1):
                start_time = time.ticks_ms()
                FireSignal.put(True)
                state=5
        # STATE 5: HOME
        elif state == 5:
            # home motors
            position=0
            angle=0
            if time.ticks_ms() > start_time + 3000:
                motors.set_position(1,position)
                motors.set_position(2,angle)
                if (abs(int(motors.get_position(1)) -  position) <= 1) and (abs(int(motors.get_position(2)) -  angle) <= 1):
                    state = 1
        
                
        
        yield